# REQ-DW8-OS-015: [Execution] Finalize State Unification and Cleanup

- **Priority:** [C]
- **Status:** [P]
- **Type:** Execution

## 1. Description

This is the final step to complete the state management refactoring. Once the `WorkflowKernel` has been fully updated to use the enhanced `WorkflowState` for all queue operations, we can safely remove the redundant queue files.

## 2. Acceptance Criteria

- The `data/pending_events.json` file is deleted.
- The `data/processed_events.json` file is deleted.
- The constants `PENDING_EVENTS_FILE` and `PROCESSED_EVENTS_FILE` at the top of `src/dw6/workflow/kernel.py` are removed.
- The system is tested to ensure it functions correctly using only the `data/workflow_state.json` file as the single source of truth.