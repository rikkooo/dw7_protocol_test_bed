import os
import shutil
import sys
import git
from pathlib import Path

# Assuming git_handler is available or its functionality is moved here
from dw6 import git_handler 

class DeployerStage:
    def __init__(self, state):
        self.state = state
        self.config = self._load_config()

    def _load_config(self):
        config = {}
        config_path = Path("docs/DEPLOYER_CONFIGURATION.md")
        if not config_path.exists():
            print(f"--- Governor: WARNING: {config_path} not found. Deployer may not function correctly. ---", file=sys.stderr)
            return config

        with open(config_path, "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.split(":", 1)
                    config[key.strip()] = value.strip()
        return config

    def validate(self, allow_failures=False):
        # First, ensure configuration is loaded.
        if not self.config:
            print("--- Governor: HALT: Deployer configuration is missing or empty. Cannot proceed. ---", file=sys.stderr)
            return False

        repo = git_handler.get_repo()
        workflow_has_changed = git_handler.check_for_workflow_changes(repo)
        is_forced_update = self.state.get("is_protocol_update") == "true"

        if is_forced_update or workflow_has_changed:
            if workflow_has_changed:
                print("--- Governor: Workflow code has changed, triggering protocol evolution. ---")
            return self._execute_protocol_evolution()
        else:
            print("--- Governor: Workflow code has not changed, triggering standard deployment. ---")
            return self._execute_standard_deployment()

    def _execute_protocol_evolution(self):
        try:
            print("--- Governor: Executing Protocol Evolution Sub-Workflow... ---")
            current_dir_name = os.path.basename(os.getcwd())
            new_protocol_name = "dw" + str(int(current_dir_name.split('_')[0][2:]) + 1)

            official_protocol_dir_base = self.config.get("OFFICIAL_PROTOCOL_DIRECTORY", "/home/ubuntu/devs/dw")
            new_protocol_dir = Path(f"{official_protocol_dir_base}/{new_protocol_name}")
            new_workflow_file = Path(f"/home/ubuntu/devs/.windsurf/workflows/start-project-{new_protocol_name}.md")

            # 1. Create new protocol directory
            if new_protocol_dir.exists():
                shutil.rmtree(new_protocol_dir)
            shutil.copytree(os.getcwd(), new_protocol_dir, ignore=shutil.ignore_patterns('.git', '__pycache__', 'venvs'))
            print(f"Created new protocol directory at {new_protocol_dir}")

            # 2. Create new start script
            with open(new_workflow_file, "w") as f:
                f.write(f"# {new_protocol_name.upper()} Project Start Workflow\n")
                f.write(f"This workflow initializes a new project using the {new_protocol_name.upper()} protocol.\n")
            print(f"Created new start script at {new_workflow_file}")

            # 3. Generate README
            with open(new_protocol_dir / "README.md", "w") as f:
                f.write(f"# {new_protocol_name.upper()} Protocol\n")
                f.write("Documentation for the new protocol version.\n")
            print(f"Generated README.md in {new_protocol_dir}")

            # 4. Git operations
            protocol_repo_url = self.config.get("OFFICIAL_PROTOCOL_REPOSITORY")
            if not protocol_repo_url:
                print("--- Governor: HALT: OFFICIAL_PROTOCOL_REPOSITORY not set in config. ---", file=sys.stderr)
                return False
            
            repo_path = "/home/ubuntu/devs/windsurf-development-workflow"
            repo = git.Repo(path=repo_path)

            commit_message = f"feat(protocol): release new protocol version {new_protocol_name}"
            files_to_commit = [str(new_protocol_dir), str(new_workflow_file)]
            git_handler.add_commit_files(files_to_commit, commit_message)

            # 5. Tagging and Dual-Push
            tag_name = f"v{new_protocol_name.replace('dw', '')}.0.0"
            repo.create_tag(tag_name, message=f"Release {tag_name}")
            print(f"Created new protocol tag: {tag_name}")

            # SMR-DW8-010.1: Push to project repository
            print("--- Governor: Pushing protocol update to project repository... ---")
            git_handler.push_to_remote(repo=repo, tags=True)

            # SMR-DW8-010.2: Push to official protocol repository
            print("--- Governor: Pushing protocol update to official repository... ---")
            official_repo_url_with_token = git_handler.get_remote_url_with_token(protocol_repo_url)
            official_remote_name = "official_protocol_repo"
            
            try:
                if official_remote_name in [remote.name for remote in repo.remotes]:
                    repo.delete_remote(official_remote_name)
                official_remote = repo.create_remote(official_remote_name, official_repo_url_with_token)
                official_remote.push(refspec=f"refs/heads/{repo.active_branch.name}:refs/heads/{repo.active_branch.name}", tags=True)
                print("--- Governor: Successfully pushed to official protocol repository. ---")
            finally:
                if official_remote_name in [remote.name for remote in repo.remotes]:
                    repo.delete_remote(official_remote_name)

            self.state.set("is_protocol_update", "false")
            return True

        except Exception as e:
            print(f"Error during protocol evolution: {e}", file=sys.stderr)
            return False

    def _synchronize_protocol_files(self):
        # This method is now deprecated. The logic has been moved to _execute_protocol_evolution.
        pass

    def _execute_standard_deployment(self):
        try:
            print("--- Governor: Executing Standard Deployment Workflow... ---")
            repo = git_handler.get_repo()
            project_repo_url = self.config.get("PROJECT_REPO_URL")
            if not project_repo_url:
                print("--- Governor: HALT: PROJECT_REPO_URL not set in config. ---", file=sys.stderr)
                return False

            # SMR-DW8-008.1: Commit all changes
            # For simplicity, we'll commit all unstaged changes. A more robust solution
            # would be to list them explicitly.
            if repo.is_dirty(untracked_files=True):
                print("--- Governor: Found uncommitted changes. Committing... ---")
                repo.git.add(A=True)
                commit_message = f"feat(cycle): complete development cycle for requirement {self.state.get('requirement_id')}"
                repo.index.commit(commit_message)
                print(f"--- Governor: Committed changes with message: '{commit_message}' ---")
            else:
                print("--- Governor: No local changes to commit. ---")

            # SMR-DW8-008.4: Push the commit to the remote repository.
            print("--- Governor: Pushing changes to remote... ---")
            git_handler.push_to_remote(repo=repo)
            
            # SMR-DW8-008.5: Apply a version tag
            # SMR-DW8-008.5: Apply a version tag
            try:
                # Get the latest tag, or fallback to v0.0.0 if no tags exist
                latest_tag_str = repo.git.describe('--tags', '--abbrev=0')
            except git.exc.GitCommandError as e:
                if "No names found, cannot describe anything" in str(e):
                    latest_tag_str = "v0.0.0"
                else:
                    raise # Re-raise other git errors

            version_parts = latest_tag_str.lstrip('v').split('.')
            major = int(version_parts[0])
            minor = int(version_parts[1])
            patch = int(version_parts[2]) if len(version_parts) > 2 else 0
            new_tag_str = f"v{major}.{minor}.{patch + 1}"
            print(f"--- Governor: Creating new version tag: {new_tag_str} ---")
            repo.create_tag(new_tag_str, message=f"Release {new_tag_str}")
            git_handler.push_to_remote(repo=repo, tags=True)

            print("--- Governor: Standard deployment completed successfully. ---")
            return True

        except Exception as e:
            print(f"Error during standard deployment: {e}", file=sys.stderr)
            return False