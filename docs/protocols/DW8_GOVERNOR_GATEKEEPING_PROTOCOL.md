# DW8 Governor Gatekeeping Protocol

**ID:** DW8_GOVERNOR_GATEKEEPING_PROTOCOL
**Status:** `Draft`

## 1. Principle: Centralized, Verifiable State Machine Control

The Governor is the ultimate authority on workflow progression. It is responsible for enforcing strict, verifiable exit criteria for each stage of the development lifecycle. Its purpose is to ensure that each stage transition is deliberate, justified, and based on tangible evidence of completion, thereby preventing context decay and unstable builds.

## 2. Architectural Mandates

- **Centralization of Logic:** All stage-gate validation logic MUST be removed from individual stage modules (e.g., `ValidatorStage.validate()`) and consolidated within the `Governor` class.
- **Deprecation of Bypasses:** The `allow_failures` flag in the `approve` command is deprecated and MUST be removed. There will be no backdoors to bypass mandatory stage validation.
- **State-Aware Transitions:** The `Governor` will orchestrate all stage transitions. Instead of a linear progression, the `Governor` will direct the workflow based on the validation outcome (e.g., a `Validator` failure returns the state to `Coder`).
- **Actionable Feedback:** When a stage transition is denied, the `Governor` MUST provide a clear, concise, and actionable reason for the denial, logged for user review.

## 3. The New `approve` Workflow

The `approve` command will trigger the following sequence:

1. The `WorkflowManager` receives the `approve` command.
2. It invokes the `Governor.request_stage_advancement()` method.
3. The `Governor` retrieves the exit criteria for the *current* stage.
4. It executes a series of check functions to validate each criterion.
5. **If all checks pass:** The `Governor` advances the state to the next logical stage (e.g., `Coder` -> `Validator`).
6. **If any check fails:** The `Governor` denies the advancement, logs the specific reason for failure, and may transition the state to a corrective stage (e.g., `Validator` -> `Coder`).

## 4. Stage-Specific Exit Criteria

This section defines the mandatory, non-bypassable exit criteria for each stage. These rules will be implemented as methods within the `Governor`.

### `Engineer` Stage Exit Criteria

- **`check_deliverable_exists()`:** At least one deliverable (e.g., a new requirement file, an architecture diagram) MUST exist in the `deliverables/engineering/` directory for the current cycle.
- **`check_requirements_updated()`:** The `docs/PROJECT_REQUIREMENTS.md` file MUST have been modified in the current Git context.

### `Researcher` Stage Exit Criteria

- **`check_deliverable_exists()`:** A research summary or report MUST exist in the `deliverables/research/` directory.

### `Coder` Stage Exit Criteria

- **`check_code_committed()`:** All code changes MUST be committed to the local Git repository. The working directory must be clean.
- **`check_deliverable_exists()`:** A changelog or implementation note MUST exist in the `deliverables/coding/` directory.

### `Validator` Stage Exit Criteria

- **`check_tests_pass()`:** The `pytest` test suite MUST run and all tests MUST pass. The `Governor` will execute the test suite directly.
- **`check_commit_reverted()`:** If tests fail, the `Governor` will automatically revert the repository to the `Validator_CommitSHA` saved by the `WorkflowKernel` before the `Coder` stage was approved.

### `Deployer` Stage Exit Criteria

- **`check_git_tagged()`:** A new, versioned Git tag MUST have been created.
- **`check_protocol_update_workflow()`:** If the `is_protocol_update` flag is true, the `Governor` MUST verify the successful execution of all steps in the `DW8_DEPLOYER_PROTOCOL` (new directory, new start script, new README).

## 5. Implementation Requirements (Execution Mode)

- **REQ-DW8-EXEC-001:** Refactor the `Governor` class to include the `request_stage_advancement` method and the stage-specific check functions.
- **REQ-DW8-EXEC-002:** Remove the `validate()` methods from all stage-specific classes (`EngineerStage`, `CoderStage`, etc.).
- **REQ-DW8-EXEC-003:** Remove the `allow_failures` parameter from the `approve` command in `dw6/main.py` and `WorkflowManager`.
- **REQ-DW8-EXEC-004:** Modify the `WorkflowKernel` to accept transition commands from the `Governor` instead of following a hardcoded path.
- **REQ-DW8-EXEC-005:** Implement the automatic Git revert mechanism in the `Governor` for `Validator` stage failures.
