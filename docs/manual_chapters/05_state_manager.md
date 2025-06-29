# Chapter 5: The State Manager

## 5.1. Role and Purpose

The State Manager (`dw6/state_manager.py`) is the definitive source of truth for the project's operational state. Its sole purpose is to load, manage, and persist the system's status to disk, ensuring that context is never lost between sessions.

It is the system's memory.

## 5.2. The State File

The State Manager's data is persisted in a single JSON file: `.dw6_state.json`.

This file is the canonical record of:

- **Current Workflow Stage:** The active stage of the state machine (e.g., `ENGINEER`, `CODER`).
- **Active Requirement:** The ID of the requirement currently being worked on.
- **Requirement Backlog:** A list of all known requirements and their current status (e.g., `pending`, `in_progress`, `completed`).
- **Session History:** A log of major events and stage transitions.

## 5.3. Key Operations

The State Manager provides a simple, clear API for the Governor to use:

- `load_state()`: Reads `.dw6_state.json` from disk and loads it into memory at the beginning of a session.
- `save_state()`: Writes the current in-memory state back to `.dw6_state.json`. The Governor calls this method after every significant change (e.g., completing a stage, adding a requirement).
- `get_current_stage()`: Returns the active workflow stage.
- `update_stage(new_stage)`: Sets the new active workflow stage.
- `get_requirement(req_id)`: Retrieves the details of a specific requirement.
- `add_requirement(requirement)`: Adds a new requirement to the backlog.

## 5.4. Integrity

The State Manager is designed for simplicity and robustness. It performs basic validation to ensure the integrity of the state file but relies on the Governor to ensure that all state transitions are logical and follow protocol. The State Manager only records the state; the Governor dictates it.
