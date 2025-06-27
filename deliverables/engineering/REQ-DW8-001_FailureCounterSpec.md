```markdown
# Technical Specification: REQ-DW8-001

**Title:** Implement a Persistent Failure Counter within the WorkflowState

**Version:** 1.0

**Date:** 2025-06-26

**Author:** Cascade

---

## 1. Overview

This document provides the technical design for implementing a persistent failure counting mechanism within the DW8 protocol. This is the foundational requirement for the "Circuit Breaker" feature, which will prevent the AI from getting stuck in repetitive failure loops.

The system will track the number of consecutive failures for critical, repeatable actions within a given workflow stage.

## 2. Design

### 2.1. Data Storage and Structure

The failure counters will be stored directly within the `logs/workflow_state.txt` file, managed by the `WorkflowState` class.

To maintain compatibility with the existing simple key-value parser, a dot-notation naming convention will be used for the counter keys.

- **Key Format:** `FailureCounters.<StageName>.<ActionName>`
- **Value:** An integer representing the number of consecutive failures.

**Example Keys:**

- `FailureCounters.Validator.pytest_execution=2`
- `FailureCounters.Deployer.mcp_push_files=1`

### 2.2. Implementation within `state_manager.py`

All logic will be contained within the `WorkflowManager` and `WorkflowState` classes.

#### 2.2.1. `WorkflowState` Modifications

No direct modifications to the class structure are needed. The existing `get(key, default)` and `set(key, value)` methods are sufficient.

#### 2.2.2. `WorkflowManager` Modifications

**A. Counter Management Functions:**

Two new helper methods will be added to `WorkflowManager`:

1.  `_increment_failure_counter(self, action_name: str)`:
    -   Constructs the key: `f"FailureCounters.{self.current_stage}.{action_name}"`
    -   Gets the current value using `self.state.get(key, 0)`.
    -   Increments the value by 1.
    -   Sets the new value using `self.state.set(key, new_value)`.

2.  `_reset_failure_counters(self, stage_name: str)`:
    -   Iterates through all keys in `self.state.data`.
    -   For each key that starts with `f"FailureCounters.{stage_name}."`, it sets the value to 0 using `self.state.set(key, 0)`.

**B. Integration into Validation Logic:**

The `_increment_failure_counter` method will be called within the `except` or failure blocks of the validation methods.

-   **Initial Target:** The `_validate_deployment` method will be the first to be integrated.

    ```python
    # In _validate_deployment
    commit_sha = git_handler.mcp_push_files(...)
    if not commit_sha:
        print("Deployment validation failed...")
        self._increment_failure_counter("mcp_push_files")
        # ... existing failure logic
    ```

**C. Integration into Stage Transition Logic:**

The `_reset_failure_counters` method will be called upon successful stage advancement.

-   **Target:** The `_advance_stage` method.

    ```python
    # In _advance_stage
    previous_stage = self.current_stage
    # ... logic to determine next_stage ...
    self.state.set("CurrentStage", next_stage)
    self._reset_failure_counters(previous_stage)
    self.state.save()
    ```

## 3. First Implementation Target

The initial implementation will focus on tracking failures for the `mcp_push_files` action within the `_validate_deployment` method, as this has been a recent point of failure.

## 4. Acceptance Criteria

- A failed `mcp_push_files` call in the `Deployer` stage correctly increments the `FailureCounters.Deployer.mcp_push_files` value in `workflow_state.txt`.
- Upon successful approval of the `Deployer` stage, the `FailureCounters.Deployer.mcp_push_files` value is reset to 0.
- The system remains stable and does not introduce regressions.
```
