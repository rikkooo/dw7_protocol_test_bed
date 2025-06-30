# REQ-DW8-OS-006: [Execution] Transition `workflow_state` to JSON

- **Priority:** [H]
- **Status:** [P]
- **Type:** Execution

## 1. Description

This requirement transitions our core state management file from its current custom format (`.workflow_state`) to a standard, robust `workflow_state.json`. This will allow for more reliable state parsing and manipulation using standard libraries.

## 2. Acceptance Criteria

- The `WorkflowState` class is refactored to read from and write to `data/workflow_state.json`.
- The old `.workflow_state` file is deprecated.
- A migration path for existing state files is considered.
