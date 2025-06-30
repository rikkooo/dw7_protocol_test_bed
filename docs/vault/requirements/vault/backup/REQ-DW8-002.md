### ID: REQ-DW8-002

- **Title:** Implement the Rehearsal State
- **Status:** `Pending`
- **Priority:** `High`
- **Details:** This requirement is to implement the `Rehearsal` state, a mandatory 'time-out' to force the AI to re-evaluate its strategy after repeated failures. This is the primary mechanism to prevent cognitive fixation.
- **SMRs:**
  - [ ] **SMR-DW8-002.1:** Create a new `RehearsalStage` class in `src/dw6/workflow/rehearsal.py`.
  - [ ] **SMR-DW8-002.2:** Add `Rehearsal` to the list of `STAGES` in `src/dw6/state_manager.py`.
  - [ ] **SMR-DW8-002.3:** Modify the `Governor`'s `approve` method to check failure counters. If a counter (e.g., `Validator.pytest`) exceeds a threshold (e.g., 3), the workflow must transition to the `Rehearsal` stage instead of failing.
  - [ ] **SMR-DW8-002.4:** The `RehearsalStage`'s `validate` method should guide the AI through a reflection process (analyzing the failure, re-evaluating the plan, proposing alternatives). For now, this can be a placeholder that simply prints the instructions.
  - [ ] **SMR-DW8-002.5:** After the `Rehearsal` stage is approved, the workflow should transition back to the stage where the failure occurred (e.g., from `Rehearsal` back to `Validator`).