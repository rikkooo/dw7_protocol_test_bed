# Chapter 6: Operational Commands

## 6.1. Overview

The primary interface for the human Principal is the command-line interface (CLI), `dw6_cli.py`. These commands are the triggers for all major workflow actions.

## 6.2. Core Commands

### `dw6-dev-sec.py start <requirement_id>`

- **Purpose:** Initiates a new work session for a specific requirement.
- **Action:** The Governor loads the system state, sets the specified requirement as active, and transitions the state machine to the first stage (typically `ENGINEER`). It then provides the AI Kernel with its initial instructions.
- **Example:** `uv run python dw6_cli.py start REQ-DW8-EXEC-001`

### `dw6-dev-sec.py approve`

- **Purpose:** To approve the completion of the current workflow stage and advance to the next.
- **Action:** The Principal uses this command after reviewing the AI's work in the current stage. The Governor performs any necessary validation for the current stage (e.g., the Living Documentation Protocol check in the `DEPLOYER` stage). If validation passes, the Governor transitions the state machine to the next stage and saves the new state.
- **Example:** `uv run python dw6_cli.py approve`

### `dw6-dev-sec.py add-req <path_to_json>`

- **Purpose:** Adds a new requirement to the project backlog.
- **Action:** The State Manager reads the requirement definition from the specified JSON file and adds it to the list of pending requirements in the state file.
- **Example:** `uv run python dw6_cli.py add-req events/REQ-DW8-DOC-010.json`

### `dw6-dev-sec.py status`

- **Purpose:** Displays the current state of the system.
- **Action:** The State Manager reads the state file and prints a summary of the current stage, the active requirement, and the status of the requirement backlog.
- **Example:** `uv run python dw6_cli.py status`
