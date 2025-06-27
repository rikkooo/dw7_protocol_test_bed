# MCP Refactoring Plan for DW7

## 1. Objective

This document outlines the plan to refactor the `dw7_protocol_test_bed` to use the `github-mcp-server` for all Git operations, eliminating the dependency on `gitpython` and the associated firewall issues.

## 2. Files to Modify

- `src/dw6/git_handler.py`
- `src/dw6/state_manager.py`

## 3. Refactoring `git_handler.py`

The following changes will be made to `git_handler.py`:

### 3.1. Add New MCP-based Functions

Two new functions will be added to the end of the file:

```python
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
    pass

def mcp_create_and_push_tag(tag_name, commit_sha, message=""):
    """
    Creates an annotated tag for a specific commit and pushes it using the GitHub MCP server.
    This function will be implemented by the agent using two calls to mcp2_fetch_json.
    """
    # Agent will implement this call.
    pass
```

### 3.2. Deprecate Old Functions

The following `gitpython`-based functions will be marked for deprecation but not yet removed:

- `add_commit_files`
- `push_to_remote`
- `get_latest_commit_hash`
- `get_local_tags_for_commit`
- `is_push_required`

## 4. Refactoring `state_manager.py`

The `_validate_deployment` function in `state_manager.py` will be completely replaced with the following code, which calls the new MCP-based functions in `git_handler.py`:

```python
    def _validate_deployment(self, allow_failures=False):
        """Validates that the latest commit has been tagged and pushes it using MCP."""
        print("Validating deployment...")

        # In the new workflow, we commit and push all changes first.
        # This will be a call to the real mcp_push_files in the Coder stage.
        commit_sha = git_handler.mcp_push_files("feat: Coder stage submission", ["src", "tests"])

        if not commit_sha:
            print("Deployment validation failed: Could not push files via MCP.", file=sys.stderr)
            if not allow_failures:
                sys.exit(1)
            return False

        # Now, create and push the tag for the new commit.
        cycle = self.state.get("CycleCounter", "1")
        tag_name = f"v1.{cycle}"
        git_handler.mcp_create_and_push_tag(tag_name, commit_sha, f"Release for cycle {cycle}")

        print(f"Deployment validation successful: Commit {commit_sha[:7]} was pushed and tagged as {tag_name}.")
        return True
```

## 5. Implementation Steps (for Coder Stage)

1.  Apply the changes to `git_handler.py` as described in section 3.1.
2.  Apply the changes to `state_manager.py` as described in section 4.
3.  Run the test suite to ensure no regressions have been introduced.
