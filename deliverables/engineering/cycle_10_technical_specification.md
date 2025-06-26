# Requirement: 10

## 1. High-Level Goal

--- System Context ---
Workflow State: Unknown
Git Branch: Unknown
Git Commit: Unknown
Git Status: Unknown
Meta-Requirements: []
----------------------

User Requirement: Fix the cycle counter to correctly increment for each new cycle.

## 2. Detailed Implementation Plan

The cycle counter is not being tracked or incremented, causing deliverables to be overwritten. This will be fixed by introducing a `CycleCounter` in the state file and using it to generate correctly versioned deliverable filenames.

### Sub-requirement 2.1: Add Cycle Counter to State Management

**File to Modify:** `src/dw6/state_manager.py`

1.  **Initialize Counter:** In the `WorkflowState.initialize_state` method, add `"CycleCounter": "1"` to the initial state dictionary. This will start the first cycle at 1.
2.  **Increment Counter:** In the `WorkflowManager.approve` method, add logic to increment the `CycleCounter`. After a successful `Deployer` stage approval, the counter in the state should be read, converted to an integer, incremented, and saved back to the state file.

### Sub-requirement 2.2: Use Cycle Counter for New Deliverables

**File to Modify:** `src/dw6/main.py`

1.  **Retrieve Counter:** In the `main` function, within the `elif args.command == "new":` block, retrieve the current `CycleCounter` value from the `WorkflowManager`'s state.
2.  **Pass Counter to Template:** Pass the retrieved `CycleCounter` as an argument to the `process_prompt` function.

**File to Modify:** `src/dw6/templates.py`

1.  **Update Function Signature:** Modify the `process_prompt` function to accept the `cycle_number` as a new parameter.
2.  **Generate Correct Filename:** Use the `cycle_number` to construct the correct path for the new technical specification, ensuring it is correctly versioned (e.g., `cycle_10_technical_specification.md`).

This comprehensive fix will ensure that each cycle is correctly numbered and that all deliverables are saved without overwriting previous work.

## 3. Guiding Principles

**Working Philosophy:** We always look to granularize projects into small, atomic requirements and sub-requirements. The more granular the requirement, the easier it is to scope, implement, test, and validate. This iterative approach minimizes risk and ensures steady, verifiable progress.
