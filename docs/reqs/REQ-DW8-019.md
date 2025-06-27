# REQ-DW8-019: [Sherlock Mode] Investigate and Enhance Git/Deployment Workflow

- **Priority:** [M]
- **Status:** [P]
- **Type:** Sherlock Mode (Investigation & Design)

## 1. Description

Our Git and deployment workflow, while functional, has several areas that require enhancement to improve clarity, robustness, and automation. This "Sherlock Mode" requirement is to investigate these areas and design formal protocols to address them.

## 2. The Plan

This investigation will cover four key areas:

### 2.1. Verbose MCP Feedback

- **Problem:** The current GitHub MCP push operation provides minimal feedback.
- **Investigation:** Research the capabilities of the `mcp5_push_files` and other related tools to see if more verbose output (e.g., list of files changed, commit SHA, link to commit) can be retrieved and displayed.

### 2.2. Workflow Update Protocol

- **Problem:** We lack a formal process for when a project's goal is to update the DW workflow itself.
- **Investigation:** Design a "double commit" protocol. This protocol will define how to safely commit changes first to the project's repository and then, upon validation, commit the updated workflow files to the official, master DW repository.

### 2.3. Dynamic README Generation

- **Problem:** The final project README is currently static.
- **Investigation:** Design a process for the Deployer to dynamically generate a comprehensive `README.md` at the end of a project. This process should involve the agent re-reading the project scope and requirements to create a summary, architecture overview, and setup/usage instructions.

### 2.4. DW Workflow Versioning

- **Problem:** Changes to the official DW workflow are not versioned, making it difficult to track history.
- **Investigation:** Design a mandatory versioning scheme (e.g., using Git tags) that must be applied every time the official DW workflow is updated.

## 3. Acceptance Criteria

- A design document is created that proposes solutions and formal protocols for each of the four areas listed above.
- New "Execution Mode" requirements are generated to implement these new protocols.
