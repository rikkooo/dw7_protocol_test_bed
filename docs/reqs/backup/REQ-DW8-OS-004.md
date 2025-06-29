# REQ-DW8-OS-004: [Execution] Refactor Kernel to Read from `pending_events.json`

- **Priority:** [C]
- **Status:** [P]
- **Type:** Execution

## 1. Description

This requirement modifies the core logic of the `WorkflowKernel`. Instead of parsing `PROJECT_REQUIREMENTS.md` to find the next task, it will now read the first entry from the `data/pending_events.json` queue. This changes the fundamental process scheduling mechanism of the system.

## 2. Acceptance Criteria

- The `WorkflowKernel`'s method for determining the next requirement is refactored.
- It now reads the `pending_events.json` file, fetches the first event ID, and sets it as the `current_event_pointer` in the state.
- The old Markdown parsing logic is completely removed.
