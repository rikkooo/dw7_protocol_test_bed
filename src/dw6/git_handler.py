import git
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
import re

# --- Environment and Repo Setup ---

def get_project_root() -> Path:
    """Returns the project root directory."""
    return Path(__file__).parent.parent.parent

def load_github_token():
    """Loads the GitHub token from the .env file."""
    env_path = get_project_root() / '.env'
    if not env_path.exists():
        print("ERROR: .env file not found. Please create one with your GITHUB_TOKEN.", file=sys.stderr)
        sys.exit(1)
    load_dotenv(dotenv_path=env_path)
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN not found in .env file.", file=sys.stderr)
        sys.exit(1)
    return token

def get_repo() -> git.Repo:
    """Initializes and returns the git.Repo object."""
    project_root = get_project_root()
    try:
        repo = git.Repo(project_root)
        return repo
    except git.InvalidGitRepositoryError:
        print(f"ERROR: Not a valid Git repository: {project_root}", file=sys.stderr)
        sys.exit(1)

def get_remote_url(repo: git.Repo = None) -> str:
    """Gets the remote URL and injects the token for authentication."""
    if repo is None:
        repo = get_repo()
    if not repo.remotes:
        print("ERROR: No remotes found in the repository.", file=sys.stderr)
        sys.exit(1)
    
    remote_url = repo.remotes.origin.url
    token = load_github_token()
    
    # Inject the token into the URL for HTTPS authentication
    if remote_url.startswith("https://"):
        url_parts = list(re.match(r"(https://)(.*)", remote_url).groups())
        authenticated_url = f"{url_parts[0]}{token}@{url_parts[1]}"
        return authenticated_url
    
    return remote_url # Return original if not HTTPS

def get_repo_info_from_remote_url(remote_url: str):
    """Extracts the repository owner and name from the remote URL."""
    # Match HTTPS URLs, including those with tokens
    match = re.search(r'github\.com[/:]([^/]+)/([^/]+?)(\.git)?$', remote_url)
    if match:
        owner, name = match.groups()[:2]
        return owner, name
    
    # Match SSH URLs
    match = re.search(r'git@github\.com:([^/]+)/([^/]+)\.git', remote_url)
    if match:
        owner, name = match.groups()
        return owner, name

    print(f"ERROR: Could not parse repository owner and name from URL: {remote_url}", file=sys.stderr)
    return None, None

# --- Git Operations ---

def get_git_status():
    """Returns the git status."""
    repo = get_repo()
    return repo.git.status()

def get_current_branch():
    """Returns the current active branch name."""
    repo = get_repo()
    return repo.active_branch.name

def get_latest_commit_sha():
    """Returns the SHA of the latest commit on the current branch."""
    repo = get_repo()
    return repo.head.commit.hexsha

def save_current_commit_sha():
    """Saves the current commit SHA to a file for the Coder to use."""
    sha = get_latest_commit_sha()
    with open("logs/current_commit.sha", "w") as f:
        f.write(sha)

# --- MCP-based Git Operations ---

def mcp_push_files(commit_message: str, file_paths: list):
    """
    Pushes specified files to the remote repository using the MCP GitHub server.
    This is a placeholder and will be implemented by the Coder.
    Returns the commit SHA on success, None on failure.
    """
    print(f"(MCP) Pushing {len(file_paths)} files with message: '{commit_message}'...")
    # In a real scenario, this would call the mcp5_push_files tool.
    # For now, we'll simulate a success and return a fake SHA.
    # In the future, this function will handle batching (REQ-DW8-008).
    return "simulated_commit_sha_1234567"

def mcp_create_and_push_tag(tag_name: str, commit_sha: str, message: str):
    """
    Creates and pushes a new tag to the remote repository using the MCP GitHub server.
    This is a placeholder and will be implemented by the Coder.
    """
    print(f"(MCP) Creating tag '{tag_name}' for commit {commit_sha[:7]} with message: '{message}'...")
    # In a real scenario, this would call the necessary MCP tools.
    # For now, we just print the action.
    pass
