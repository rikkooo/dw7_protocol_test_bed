# REQ-DW8-VAL-001: End-to-End Workflow Engine Validation

## 1. Requirement

Perform a complete, end-to-end run of the DW8 workflow to validate that the recent engine fixes, particularly concerning git operations, credential handling, and testing, are functioning correctly in a live cycle.

## 2. Justification

The recent development cycle involved significant, low-level changes to the git handler and its interaction with the testing framework. While individual components now pass unit tests, it is critical to verify that they operate correctly as part of the integrated workflow state machine. This validation run will serve as the final confirmation that the system is stable and ready for further development.

## 3. Acceptance Criteria

- [ ] The workflow can be initiated using the `dw6` CLI.
- [ ] A simple task (e.g., creating a new file) can be defined in the `Engineer` stage.
- [ ] The task can be researched, coded, and validated in their respective stages.
- [ ] The `Validator` stage correctly executes the `pytest` suite and passes.
- [ ] The `Deployer` stage successfully commits and pushes the new file to the remote repository.
- [ ] The entire workflow completes without any errors or unexpected prompts (after initial setup).
