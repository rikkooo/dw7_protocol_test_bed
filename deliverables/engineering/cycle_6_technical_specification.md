# Requirement: 6

## 1. High-Level Goal

--- System Context ---
Workflow State: Unknown
Git Branch: Unknown
Git Commit: Unknown
Git Status: Unknown
Meta-Requirements: []
----------------------

User Requirement: Overhaul the Deployer Stage Git Integration to use the github-mcp-server instead of gitpython for remote operations.

## 2. Detailed Implementation Plan

The current implementation of the `Deployer` stage fails because the `_get_authenticated_remote_url` function in `src/dw6/git_handler.py` uses a fragile string replacement to create the authenticated Git URL. This results in a malformed URL that `git` cannot process.

This will be fixed by refactoring the function to use Python's robust `urllib.parse` library for URL manipulation.

### Sub-requirement 2.1: Refactor `_get_authenticated_remote_url`

**File to Modify:** `src/dw6/git_handler.py`

1.  **Import necessary library:** Add `from urllib.parse import urlparse, urlunparse` to the top of the file.
2.  **Rewrite the function logic:**
    *   The function will still retrieve the `GITHUB_TOKEN` and the `origin` remote URL as before.
    *   It will then parse the remote URL using `urlparse()`.
    *   A new `netloc` (network location) string will be constructed in the format: `{token}@{hostname}`. For example: `ghp_YourToken@github.com`.
    *   The parsed URL components will be reassembled into a new, valid URL string using `urlunparse()`, with the new `netloc` replacing the old one.
    *   This new, correctly-formed URL will be returned.

This change will ensure that all subsequent `git fetch` and `git push` calls use a valid URL, permanently fixing the deployment failures.

## 3. Guiding Principles

**Working Philosophy:** We always look to granularize projects into small, atomic requirements and sub-requirements. The more granular the requirement, the easier it is to scope, implement, test, and validate. This iterative approach minimizes risk and ensures steady, verifiable progress.
