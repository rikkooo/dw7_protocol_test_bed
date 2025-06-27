import git
import sys
import os
import time
from dotenv import load_dotenv
from pathlib import Path
import re
from urllib.parse import urlparse, urlunparse

# This is a placeholder for the real MCP client provided by the environment.
# It allows the code to be syntactically correct and for tests to patch 'dw6.git_handler.mcp5'.
try:
    import mcp5
except ImportError:
    # In a real execution, this would be an issue. For testing, it's fine as it will be mocked.
    mcp5 = None

# --- Environment and Repo Setup ---

def get_project_root() -> Path:
    """Returns the project root directory."""
    return Path(__file__).parent.parent.parent

def load_github_token(repo_path=None):
    """Loads the GitHub token from the .env file, prompting the user if not found."""
    if repo_path:
        env_path = Path(repo_path) / '.env'
    else:
        env_path = get_project_root() / '.env'

    load_dotenv(dotenv_path=env_path)
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("--- Governor: GITHUB_TOKEN not found in .env file or environment. ---")
        token = input("Please enter your GitHub Personal Access Token: ").strip()
        if not token:
            print("ERROR: No GitHub token provided. Cannot proceed.", file=sys.stderr)
            sys.exit(1)
        save_github_token(token, env_path)
    
    return token

def save_github_token(token, env_path):
    """Saves the GitHub token to the .env file."""
    print(f"--- Governor: Saving GITHUB_TOKEN to {env_path} ---")
    with open(env_path, "a") as f:
        if os.stat(env_path).st_size != 0:
            f.write("\n")
        f.write(f'GITHUB_TOKEN="{token}"\n')
    # Update the environment for the current process
    os.environ["GITHUB_TOKEN"] = token

def get_repo() -> git.Repo:
    """Initializes and returns the git.Repo object."""
    project_root = get_project_root()
    try:
        repo = git.Repo(project_root)
        return repo
    except git.InvalidGitRepositoryError:
        print(f"ERROR: Not a valid Git repository: {project_root}", file=sys.stderr)
        sys.exit(1)



def get_repo_info_from_remote_url(remote_url: str):
    """Extracts the repository owner and name from the remote URL."""
    # Match HTTPS URLs, including those with tokens
    match = re.search(r'github\.com/([^/]+)/([^/]+?)(?:\.git)?$', remote_url)
    if match:
        owner, repo_name = match.groups()
        return owner, repo_name.replace(".git", "")
    return None, None

# --- Core Git Functions (using gitpython) ---

def add_commit_files(files, message):
    """Adds and commits a list of files."""
    repo = get_repo()
    try:
        repo.git.add(files)
        repo.git.commit('-m', message)
        print(f"[GIT] Committed changes for files {files} with message: '{message}'")
    except git.exc.GitCommandError as e:
        print(f"ERROR: Failed to commit files. {e}", file=sys.stderr)
        if "nothing to commit" in str(e):
            print("INFO: No changes to commit.")
        else:
            sys.exit(1)

def push_to_remote(repo=None, tags=False):
    """Pushes the current branch and optionally tags to the remote repository."""
    if repo is None:
        repo = get_repo()

    remote = repo.remotes.origin
    
    # Retry logic for authentication
    for attempt in range(2):
        try:
            # Load the token to ensure the credential helper is up-to-date
            load_github_token(repo_path=repo.working_dir)
            
            if tags:
                print("--- Governor: Pushing tags to remote... ---")
                result = remote.push(tags=True)
            else:
                print(f"--- Governor: Pushing branch '{repo.active_branch.name}' to remote... ---")
                result = remote.push(refspec=f'{repo.active_branch.name}:{repo.active_branch.name}')

            # Check for errors in the push result
            for info in result:
                if info.flags & git.PushInfo.ERROR:
                    raise git.exc.GitCommandError(f"Push failed: {info.summary}")
            
            print("--- Governor: Push successful. ---")
            return True

        except git.exc.GitCommandError as e:
            print(f"Push failed (attempt {attempt + 1}/2): {e}", file=sys.stderr)
            if 'Authentication failed' in str(e) and attempt == 0:
                # Force a token re-prompt on the next iteration
                print("--- Governor: Authentication failed. Clearing token and retrying. ---")
                os.environ.pop('GITHUB_TOKEN', None)
                (Path(repo.working_dir) / '.env').unlink(missing_ok=True)
            else:
                print("FATAL: Git push failed after multiple retries.", file=sys.stderr)
                return False
        except Exception as e:
            print(f"An unexpected error occurred during push: {e}", file=sys.stderr)
            return False
            
    return False

def get_latest_commit_hash(repo: git.Repo = None):
    """Gets the hash of the latest commit."""
    if repo is None:
        repo = get_repo()
    return repo.head.commit.hexsha

def get_local_tags_for_commit(commit_hash, repo: git.Repo = None):
    """Gets all local tags pointing to a specific commit."""
    if repo is None:
        repo = get_repo()
    return [tag.name for tag in repo.tags if tag.commit.hexsha == commit_hash]

def is_push_required(repo: git.Repo = None):
    """Checks if the local branch is ahead of the remote branch."""
    if repo is None:
        repo = get_repo()
    
    try:
        repo.remotes.origin.fetch()
    except git.exc.GitCommandError as e:
        print(f"Warning: Could not fetch from remote to check status: {e}", file=sys.stderr)
        return True # Assume push is required if fetch fails

    local_commit = repo.head.commit
    remote_branch = f'origin/{repo.active_branch.name}'
    
    try:
        remote_commit = repo.commit(remote_branch)
        return local_commit != remote_commit
    except git.exc.BadName:
        # Remote branch doesn't exist, so a push is definitely required.
        return True

def save_current_commit_sha():
    """Saves the current commit SHA to a file for the Coder stage."""
    sha = get_latest_commit_hash()
    sha_file_path = get_project_root() / "logs" / "last_commit_sha.txt"
    sha_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(sha_file_path, "w") as f:
        f.write(sha)
    print(f"Saved current commit SHA for Coder stage: {sha[:7]}")

def get_last_commit_sha():
    """Reads the last saved commit SHA from the Coder stage."""
    sha_file = get_project_root() / 'logs' / 'last_commit_sha.txt'
    try:
        with open(sha_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Warning: logs/last_commit_sha.txt not found. Cannot determine changes.", file=sys.stderr)
        return None

def get_changes_since_last_commit(commit_sha):
    """Gets the changed files and diff since the last saved commit."""
    repo = get_repo()
    if not commit_sha:
        print("Warning: No commit SHA provided. Cannot determine changes.", file=sys.stderr)
        return [], ""

    try:
        diff_output = repo.git.diff(commit_sha, 'HEAD', name_only=True)
        changed_files = diff_output.split('\n')
        
        full_diff = repo.git.diff(commit_sha, 'HEAD')
        
        return changed_files, full_diff
    except FileNotFoundError:
        print("Warning: last_commit_sha.txt not found. Cannot determine changes.", file=sys.stderr)
        return [], ""

def check_for_workflow_changes(repo: git.Repo):
    """Checks if any files in the src/dw6/ directory have changed since the last cycle."""
    last_commit_sha = get_last_commit_sha()
    if not last_commit_sha:
        return False # Cannot determine changes, assume none

    try:
        # Check for changes in the specified directory since the last commit
        changed_files = repo.git.diff(last_commit_sha, 'HEAD', '--name-only', 'src/dw6/').split('\n')
        # Return True if the list of changed files is not empty
        return bool([f for f in changed_files if f])
    except git.GitCommandError as e:
        print(f"Error checking for workflow changes: {e}", file=sys.stderr)
        return False

def commit_and_push_deliverable(file_path, stage_name, requirement_id):
    """Commits and pushes a deliverable file."""
    message = f"docs(cycle-{requirement_id}): Add {stage_name.lower()} deliverable for cycle {requirement_id}"
    print(f"[GIT] Committing deliverable: {file_path}")
    add_commit_files([file_path], message)
    print("[GIT] Pushing deliverable to remote...")
    push_to_remote()

# --- Core Git Functions (using GitHub MCP) ---

def get_repo_owner_and_name():
    """Gets the repository owner and name from the remote URL."""
    remote_url = get_remote_url()
    if not remote_url:
        print("ERROR: Could not determine remote URL.", file=sys.stderr)
        sys.exit(1)
    owner, repo_name = get_repo_info_from_remote_url(remote_url)
    if not owner or not repo_name:
        print(f"ERROR: Could not parse owner and repo from URL: {remote_url}", file=sys.stderr)
        sys.exit(1)
    return owner, repo_name

def mcp_push_files(commit_message, file_paths, branch='main'):
    """
    Commits and pushes a list of files to the remote repository using the GitHub MCP server.
    This function will be implemented by the agent using the mcp5_push_files tool.
    """
    # Agent will implement this call.
    print("MCP: Pushing files (placeholder)...")
    return "mcp_commit_sha_placeholder" # Placeholder
    pass

def mcp_create_and_push_tag(tag_name, commit_sha, message=""):
    """
    Creates an annotated tag for a specific commit and pushes it using the GitHub MCP server.
    This function will be implemented by the agent using two calls to mcp2_fetch_json.
    """
    # Agent will implement this call.
    print(f"MCP: Creating and pushing tag {tag_name} (placeholder)...")
    pass