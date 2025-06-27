import os
import shutil
import sys
from pathlib import Path
import git
from dw6 import git_handler

def _execute_protocol_evolution(self):
    try:
        repo = git.Repo(os.getcwd())

        # 1. Determine the new protocol version from git tags
        latest_version = -1
        for tag in repo.tags:
            if tag.name.startswith('v') and tag.name.count('.') == 2:
                try:
                    version_str = tag.name[1:].split('.')[0]
                    version = int(version_str)
                    if version > latest_version:
                        latest_version = version
                except (ValueError, IndexError):
                    continue

        new_version = latest_version + 1
        new_protocol_name = f"dw{new_version}"
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
        git_handler.push_to_remote(files=['.'], message='Pushing protocol update to project repository', repo=repo)

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
