# REQ-DW8-OS-003: [Execution] Create Migration Script for Existing Requirements

- **Priority:** [C]
- **Status:** [P]
- **Type:** Execution

## 1. Description

To transition to the new OS model without losing our project history and pending tasks, we need a one-time migration script. This script will parse the existing `docs/PROJECT_REQUIREMENTS.md` and the individual `/reqs/*.md` files, converting them into the new JSON event format.

## 2. Acceptance Criteria

- A Python script is created (e.g., `scripts/migrate_reqs_to_json.py`).
- When run, the script successfully populates `data/pending_events.json` and `data/processed_events.json` with the data from the old Markdown files.
- The script is idempotent and can be run safely multiple times.
