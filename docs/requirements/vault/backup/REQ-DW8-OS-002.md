# REQ-DW8-OS-002: [Execution] Replace `PROJECT_REQUIREMENTS.md` with Event Queues

- **Priority:** [C]
- **Status:** [P]
- **Type:** Execution

## 1. Description

This requirement is to replace the single, monolithic `PROJECT_REQUIREMENTS.md` file with a more robust and efficient dual-queue system implemented in JSON. This is a foundational step in the OS refactoring.

- **`pending_events.json`**: Will hold the list of tasks to be processed.
- **`processed_events.json`**: Will hold a log of completed tasks.

## 2. Acceptance Criteria

- The `docs/PROJECT_REQUIREMENTS.md` file is removed from the system's logic (it can be archived).
- Two new files, `data/pending_events.json` and `data/processed_events.json`, are created.
- The system is able to initialize with these new empty files.

## 3. Sherlock Mode Findings (2025-06-28)

- **Contradiction Identified:** The investigation revealed a critical architectural flaw. The system has two competing sources of truth for the event queue.
- **State Manager (`WorkflowManager`):** Correctly initializes the `WorkflowKernel` with a `PendingEvents` list stored within the primary `data/workflow_state.json` file.
- **Kernel (`WorkflowKernel`):** While the main workflow uses the state-provided list, several key methods (`_complete_event_in_queue`, `_create_red_flag_requirement`) incorrectly read from and write to the separate `data/pending_events.json` and `data/processed_events.json` files.
- **Conclusion:** This violation of the "single source of truth" principle is the root cause of recent instability and context loss. The system's state management must be unified before proceeding.
