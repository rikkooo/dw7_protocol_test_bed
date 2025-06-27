import sys
from dw6 import git_handler
import git

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
