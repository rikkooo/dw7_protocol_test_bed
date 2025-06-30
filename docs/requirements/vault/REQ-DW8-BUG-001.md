# [REQ-DW8-BUG-001] Fix Incorrect Command Invocation in Governor Rules

**Status:** Pending
**Priority:** Critical

## Details

The Governor's RULES in `src/dw6/state_manager.py` are hardcoded to use the incorrect command invocation `uv run python -m dw6.main ...`. This must be replaced with the correct script entry point `dw6 ...` as defined in `pyproject.toml`. This is a foundational bug that prevents the entire workflow from executing correctly.

## Sub-Requirements

- SMR-BUG-001.1: Read `src/dw6/state_manager.py`.
- SMR-BUG-001.2: In the `Governor.RULES` dictionary, replace all instances of `uv run python -m dw6.main` with `dw6`.
