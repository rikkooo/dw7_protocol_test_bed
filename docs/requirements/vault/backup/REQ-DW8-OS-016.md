# REQ-DW8-OS-016: [Execution] Implement the Context Integrity Protocol

- **Priority:** [C]
- **Status:** [P]
- **Type:** Execution

## 1. Description

To combat context window resets ("memory loss"), which pose a critical threat to project stability, we will implement a proactive Context Integrity Protocol. This protocol will provide a reliable, automated mechanism for detecting and recovering from context loss, ensuring the AI engineer remains synchronized with the project's state and goals.

## 2. Acceptance Criteria

- **SMR-1: Create a `check-context` CLI Command.**
  - A new command, `uv run python -m dw6.main check-context`, is added to `cli.py`.
  - This command will trigger the Context Integrity Protocol.

- **SMR-2: Implement the "Cognitive Checkpoint".**
  - A new key, `CognitiveCheckpoint`, is added to the `data/workflow_state.json` file. Its value will be a secret phrase or key (e.g., "Riko").
  - The `check-context` command logic will first attempt to access and verify this key from its internal memory.

- **SMR-3: Implement the "Context Refresh" Procedure.**
  - If the Cognitive Checkpoint fails, the system automatically triggers a context refresh.
  - This procedure involves systematically reading a predefined list of critical project documents to rebuild the AI's understanding. The initial list will include:
    - `docs/ARCHITECTURE.md`
    - All files in `docs/protocols/`
    - All `REQ-DW8-OS-*` files in `docs/reqs/`

- **SMR-4: Generate a Context Restoration Report.**
  - After the refresh procedure is complete, the AI will generate a concise summary of its restored understanding.
  - This report will be presented to the user for verification, confirming that context has been successfully rebuilt before proceeding with any other tasks.