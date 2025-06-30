### ID: REQ-DW8-001

- **Title:** Implement a persistent failure counter
- **Status:** `Pending`
- **Priority:** `High`
- **Details:** This requirement is to implement a persistent failure counter within the `.workflow_state` for critical, repeatable actions. This is the foundational step for the Rehearsal state and Escalation Protocol. The counter should track consecutive failures for specific, named operations.
- **SMRs:**
  - [ ] **SMR-DW8-001.1:** Modify the `WorkflowState` class (or its manager) to include a nested dictionary for `FailureCounters`.
  - [ ] **SMR-DW8-001.2:** Implement methods to increment a specific counter (e.g., `increment_failure_counter('pytest')`) and reset a counter (e.g., `reset_failure_counter('pytest')`).
  - [ ] **SMR-DW8-001.3:** Modify the `Validator` stage to use this new counter when `pytest` fails.
  - [ ] **SMR-DW8-001.4:** Ensure the counters are correctly persisted to the `.workflow_state` file.