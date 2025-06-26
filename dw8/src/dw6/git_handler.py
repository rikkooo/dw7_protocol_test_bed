import git
import sys
import os
import time
from dotenv import load_dotenv
from pathlib import Path
import re
from urllib.parse import urlparse, urlunparse

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
    
    remote_url = repo.remotes.origin.url.strip()
    token = load_github_token()
    
    # Inject the token into the URL for HTTPS authentication
    if remote_url.startswith("https://"):
        try:
            parts = urlparse(remote_url)
            new_netloc = f"{token}@{parts.netloc}"
            path = parts.path
            if path.endswith('/'):
                path = path[:-1]
            authenticated_url = urlunparse(parts._replace(netloc=new_netloc, path=path))
            return authenticated_url
        except Exception as e:
            print(f"ERROR: Could not parse remote URL '{remote_url}'. Error: {e}", file=sys.stderr)
            sys.exit(1)

    return remote_url

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

def push_to_remote(repo: git.Repo = None, retries=3, delay=5):
    """Pushes changes to the remote repository with retry logic."""
    if repo is None:
        repo = get_repo()
    
    remote_url = get_remote_url(repo)
    current_branch = repo.active_branch.name

    for attempt in range(retries):
        try:
            print(f"[GIT] Pushing to {current_branch} (Attempt {attempt + 1}/{retries})...")
            repo.git.push(remote_url, current_branch, '--tags', '--force')
            print("[GIT] Push successful.")
            return
        except git.exc.GitCommandError as e:
            print(f"ERROR: Failed to push to remote. {e}", file=sys.stderr)
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("FATAL: All push attempts failed.", file=sys.stderr)
                sys.exit(1)

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
    with open("logs/last_commit_sha.txt", "w") as f:
        f.write(sha)
    print(f"Saved current commit SHA for Coder stage: {sha[:7]}")

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