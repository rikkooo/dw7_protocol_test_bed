# REQ-DW8-020 - Implement Context Window Canary & System Health Check

**Type:** Standard
**Status:** Pending

## Description

To combat context loss, the workflow will use a 'canary' value (like a password) stored in its state. At key points, the Governor will check if the agent remembers the canary. A failure triggers a 'Small Boot' procedure to perform a full context refresh and system health check.

## Acceptance Criteria

- A canary value is stored in workflow_state.json.
- The kernel has a mechanism to validate the agent's memory of the canary.
- A failure triggers a 'Small Boot' state that reloads detailed project context, architecture, and recent conversation history.
- During 'Small Boot', a comprehensive system health check (git, env, dependencies) is performed.