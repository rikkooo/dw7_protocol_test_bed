# REQ-DW8-019 - Implement Personalization and Workflow-Managed Memory

**Type:** Standard
**Status:** Pending

## Description

The workflow should have its own persistent memory to store user-specific data (like name) and project context. It should use this data to provide personalized greetings and summaries, including acknowledging time since the last session.

## Acceptance Criteria

- The system prompts for and stores the user's name in a persistent, project-local file.
- On startup, the kernel greets the user by name and can comment on the time since the last session.
- The kernel provides a concise summary of the project status on startup.