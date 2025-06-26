# Requirement: 9

## 1. High-Level Goal

--- System Context ---
Workflow State: Unknown
Git Branch: Unknown
Git Commit: Unknown
Git Status: Unknown
Meta-Requirements: []
----------------------

User Requirement: Fix the Governor's inflexible rules for the Validator stage to allow the correct pytest command.

## 2. Detailed Implementation Plan

The `Validator` stage is currently blocked because the Governor's rules enforce a known-failing command (`uv run pytest`). This will be fixed by updating the rule to use the correct, working command.

### Sub-requirement 2.1: Update Validator Stage Rule

**File to Modify:** `src/dw6/state_manager.py`

1.  **Locate the Governor Rules:** The change will be made in the `RULES` dictionary within the `Governor` class.
2.  **Update the Command:** The value for the `"Validator"` key will be changed from `["uv run pytest"]` to `["uv run python -m pytest"]`.

This simple change will resolve the critical workflow deadlock and allow the `Validator` stage to execute correctly.

## 3. Guiding Principles

**Working Philosophy:** We always look to granularize projects into small, atomic requirements and sub-requirements. The more granular the requirement, the easier it is to scope, implement, test, and validate. This iterative approach minimizes risk and ensures steady, verifiable progress.
