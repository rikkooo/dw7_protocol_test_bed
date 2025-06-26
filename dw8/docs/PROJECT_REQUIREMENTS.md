# DW8 Protocol Master Requirements

This document is the single source of truth for all project requirements. It is dynamically managed and re-prioritized as new tasks emerge.

---

### ID: REQ-DW8-012

- **Title:** Implement Atomic Granularity Principle
- **Status:** `Pending`
- **Priority:** `Critical`
- **Details:** The AI must break down every large requirement into the smallest possible, independently solvable, and verifiable sub-requirements. This "laser focus" on atomic tasks will prevent the agent from getting lost in complexity and will make its work easier to validate.
- **SMRs:**
  - [ ] Before starting work on any new requirement, the AI must first analyze it for complexity.
  - [ ] If the requirement is not sufficiently granular, the AI must break it down into smaller sub-requirements and add them to this master list.

---

### ID: REQ-DW8-013

- **Title:** Implement Mandatory Context Refresh Protocol
- **Status:** `Pending`
- **Priority:** `Critical`
- **Details:** At the start of every new work cycle, before taking any action, the AI must perform a full context refresh. This will serve as a shield against context decay.
- **SMRs:**
  - [ ] At the beginning of each new session or cycle, the AI will re-read this `PROJECT_REQUIREMENTS.md` file in its entirety.
  - [ ] The AI will then provide a brief summary of the overall project status, the last completed task, and the immediate next task.

---

### ID: REQ-DW8-014

- **Title:** Authorize `approve` Command in Validator Stage
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The DW7 protocol has a bug where the `Validator` stage is a dead end. The `approve` command is not authorized, preventing the workflow from advancing. This SMR will fix the authorization rule.
- **SMRs:**
  - [ ] Modify the `Governor.RULES` dictionary in `src/dw6/state_manager.py` to add `"uv run python -m dw6.main approve"` to the list of allowed commands for the `Validator` stage.

---

### ID: REQ-DW8-015

- **Title:** Implement `Validator` to `Deployer` Stage Advancement
- **Status:** `Halted`
- **Priority:** `High`
- **Details:** The DW7 protocol has a bug where there is no logic to handle the transition from `Validator` to `Deployer`. This SMR will add the missing advancement logic.
- **SMRs:**
  - [ ] Modify the `WorkflowManager.approve` method in `src/dw6/state_manager.py` to include a new condition (`elif self.current_stage == "Validator":`) that calls `self._advance_stage()`.

---

### ID: REQ-DW8-016

- **Title:** Fix Flawed Mock in Environment Test
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The test `test_state_initialization_creates_env_and_persists_path` is failing because it incorrectly mocks `os.path.exists` when the code uses `pathlib.Path.exists`.
- **SMRs:**
  - [ ] In `tests/test_environment_management.py`, change the patch from `@patch('os.path.exists')` to `@patch('pathlib.Path.exists')`.

---

### ID: REQ-DW8-017

- **Title:** Authorize `approve` Command in Coder Stage
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The protocol incorrectly forbids the `approve` command in the `Coder` stage, making it impossible to advance the workflow. This must be corrected in the Governor's rules.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, add `"uv run python -m dw6.main approve"` to the `Governor.RULES` for the `Coder` stage.

---

### ID: REQ-DW8-018

- **Title:** Fix `TypeError` in Deployment Validation Test
- **Status:** `Deployed`
- **Priority:** `Medium`
- **Details:** The test `test_failure_counter_increment_and_reset` incorrectly calls `_validate_deployment` with an `allow_failures` argument, which the method does not accept.
- **SMRs:**
  - [ ] In `tests/test_state_manager_integration.py`, remove the `allow_failures=True` argument from the call to `manager._validate_deployment()`.

---

### ID: REQ-DW8-019

- **Title:** Correct Test Validation Logic for Allowed Failures
- **Status:** `Deployed`
- **Priority:** `Medium`
- **Details:** The `_validate_tests` method incorrectly returns `True` when `allow_failures` is set and tests fail. It should return `False` to correctly indicate a validation failure, even if the workflow is allowed to continue.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, inside the `_validate_tests` method, change the line `return True` within the `if allow_failures:` block to `return False`.

---

### ID: REQ-DW8-020

- **Title:** Declare `pytest` as a Test Dependency
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The test suite cannot run because `pytest` is not installed in the virtual environment. This is because it was never declared as a dependency in `pyproject.toml`.
- **SMRs:**
  - [ ] Add a `[project.optional-dependencies]` table to `pyproject.toml`.
  - [ ] Define a `test` group within this table that includes `"pytest"`.

---

### ID: REQ-DW8-021

- **Title:** Declare `GitPython` as a Core Dependency
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The application fails on startup because the `git` module (from the `GitPython` library) is not installed. It was never declared as a core dependency in `pyproject.toml`.
- **SMRs:**
  - [ ] Add `"GitPython"` to the `dependencies` list under the `[project]` table in `pyproject.toml`.

---

### ID: REQ-DW8-022

- **Title:** Fix Invalid `pyproject.toml` by Merging Duplicate Sections
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The `pyproject.toml` file is invalid because it contains two `[project.optional-dependencies]` sections. This prevents correct parsing of dependencies and causes installation failures.
- **SMRs:**
  - [ ] Merge the two `[project.optional-dependencies]` sections into a single, comprehensive section.

---

### ID: REQ-DW8-023

- **Title:** Refactor State Manager to Use Lazy Imports
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The application cannot start because the environment setup script (`cli.py` -> `state_manager.py`) has a circular dependency: it imports modules that are only available *after* the environment has been set up. This will be fixed by moving the imports into the methods that use them (lazy importing).
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, move `from dw6 import git_handler` from the top of the file into the `_generate_deliverable` and `_validate_deployment` methods.

---

### ID: REQ-DW8-024

- **Title:** Fix `NameError` in `save_current_commit_sha`
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The `save_current_commit_sha` method in `WorkflowManager` calls `git_handler` without importing it, a bug introduced by the lazy-loading refactor.
- **SMRs:**
  - [ ] Add `from dw6 import git_handler` to the top of the `save_current_commit_sha` method.

---

### ID: REQ-DW8-025

- **Title:** Fix Incorrect Success Logic in `_validate_deployment`
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The `_validate_deployment` method does not check the return value from `git_handler.mcp_push_files`. It assumes success unless an exception is thrown, causing tests that simulate failure to fail.
- **SMRs:**
  - [ ] Add a check for a falsy `commit_sha` and return `False` immediately after the `mcp_push_files` call.

---

### ID: REQ-DW8-026

- **Title:** Fix Incorrect Patch Target in State Manager Tests
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** Tests in `test_state_manager.py` fail with an `AttributeError` because they try to patch `dw6.state_manager.git_handler`, which no longer exists after the lazy-loading refactor.
- **SMRs:**
  - [ ] Change the patch target to `dw6.git_handler`.

---

### ID: REQ-DW8-027

- **Title:** Fix Double Initialization in Environment Tests
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The test `test_state_initialization_creates_env_and_persists_path` in `test_environment_management.py` causes `initialize_state` to be called twice.
- **SMRs:**
  - [ ] Refactor the test setup to prevent the double call to `initialize_state`.

---

### ID: REQ-DW8-028

- **Title:** Fix PermissionError in Coder Deliverable Test
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The test `test_generate_coder_deliverable` fails with a `PermissionError` because the mock for `WorkflowState.get` does not correctly provide the `CurrentStage` when the `Governor` is initialized.
- **SMRs:**
  - [ ] In `tests/test_state_manager.py`, update the `side_effect` of the `mock_state.get` to correctly return 'Coder' for the 'CurrentStage' key.

---

### ID: REQ-DW8-029

- **Title:** Fix Skipped Deliverable in Coder Approval Test
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The test `test_approve_coder_stage_creates_deliverable` fails because the deliverable file is never created, as the mock state is missing a commit SHA for the Coder stage.
- **SMRs:**
  - [ ] In `tests/test_state_manager_integration.py`, add `CommitSHA.Coder` with a dummy value to the mocked state dictionary.

---

### ID: REQ-DW8-030

- **Title:** Refactor and Fix Failure Counter Test
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The test `test_failure_counter_increment_and_reset` is flawed. It calls a private validation method directly instead of the public `approve` method, so the failure handling logic is never triggered.
- **SMRs:**
  - [ ] Refactor the test to call `manager.approve()`.
  - [ ] Correct the assertion to check for the dynamically generated failure counter key.
  - [ ] Fix the duplicate `if self.current_stage == "Validator":` block in `_validate_stage` in `state_manager.py`.

---

### ID: REQ-DW8-031

- **Title:** Fix Missing Commit SHA in Unit Test
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The `test_generate_coder_deliverable` unit test in `test_state_manager.py` fails because the mock state is missing a `CommitSHA.Coder` value, causing the deliverable generation to be skipped.
- **SMRs:**
  - [ ] Add `CommitSHA.Coder` to the mock data dictionary in the test.

---

### ID: REQ-DW8-032

- **Title:** Fix Brittle `save` Assertion in Integration Test
- **Status:** `Deployed`
- **Priority:** `Medium`
- **Details:** The test `test_approve_coder_stage_creates_deliverable` asserts `save()` is called once, but it is correctly called twice. This makes the test brittle.
- **SMRs:**
  - [ ] Change the assertion from `assert_called_once()` to `assertTrue(mock_state_instance.save.called)`.

---

### ID: REQ-DW8-033

- **Title:** Fix Incorrect Failure Counter Key Generation
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** When a validation function returns `False`, the failure counter key is generated incorrectly (e.g., `...default` instead of `..._validate_deployment`).
- **SMRs:**
  - [ ] Implement a `_get_validation_func_name()` method in `WorkflowManager` to correctly identify the validation function for the current stage.
  - [ ] Update the `approve` method's failure handling logic to use this new method for generating the failure key.

---

### ID: REQ-DW8-034

- **Title:** Fix Flawed Mocking in Failure Counter Test
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The test `test_failure_counter_increment_and_reset` fails because the mock for `WorkflowState.increment` does not update the underlying data dictionary, causing the assertion to fail.
- **SMRs:**
  - [ ] In `tests/test_state_manager_integration.py`, add a `side_effect` to the `mock_state_instance.increment` that correctly modifies the mock data dictionary.

---

### ID: REQ-DW8-035

- **Title:** Decouple Workflow Manager from Process Control
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The `_advance_stage` method in `WorkflowManager` incorrectly calls `sys.exit(0)`, making the class untestable and violating separation of concerns.
- **SMRs:**
  - [ ] Remove the `sys.exit(0)` call from `_advance_stage`.
  - [ ] Ensure the workflow correctly cycles back to the `Engineer` stage after `Deployer` completes.

---

### ID: REQ-DW8-036

- **Title:** Perfect the Failure Counter Test
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The test `test_failure_counter_increment_and_reset` incorrectly calls a private method and triggers a `SystemExit`. It must be refactored to simulate a full, successful approval cycle to test the counter reset.
- **SMRs:**
  - [ ] Reconfigure the mocks to simulate a successful deployment on the second `approve()` call.
  - [ ] Assert that the failure counter is correctly reset to 0 after the successful stage advance.

---

### ID: REQ-DW8-037

- **Title:** Correct Final Assertion in Failure Counter Test
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The test `test_failure_counter_increment_and_reset` incorrectly asserts that the failure counter key is deleted on reset (`assertIsNone`). The implementation correctly resets the value to '0'.
- **SMRs:**
  - [x] Change the final assertion to `assertEqual(..., '0')`.

---

### ID: REQ-DW8-038

- **Title:** Synchronize Virtual Environment with Dependencies
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The `Deployer` stage failed with a `ModuleNotFoundError` because the virtual environment was not up-to-date with the `pyproject.toml` file, specifically missing the `GitPython` dependency.
- **SMRs:**
  - [x] Ran `pip install -e .[test]` to synchronize the environment.

---

### ID: REQ-DW8-039

- **Title:** Use Correct Python Interpreter for CLI Execution
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The `Deployer` stage was consistently failing with `ModuleNotFoundError: No module named 'git'` because the CLI script was being invoked with the system's default Python interpreter instead of the one located in the project's virtual environment. This prevented the script from finding its installed dependencies.
- **SMRs:**
  - [x] Corrected the `run_command` call to use the full path to the virtual environment's Python executable (`/home/ubuntu/venvs/dw7_protocol_test_bed/bin/python`).

---

### ID: REQ-DW8-011

- **Title:** Implement Robust and Persistent Virtual Environment Management
- **Status:** `Pending`
- **Priority:** `Critical`
- **Details:** The current workflow suffers from "environment context decay." The AI agent repeatedly fails to use the correct, activated Python virtual environment, leading to persistent dependency and execution errors. The protocol must be updated to manage the virtual environment as a core, persistent component.
- **SMRs:**
  - [ ] **Standardize Environment Location:** The project start script (`start-project-dwX.md`) must define a standard, predictable location for the virtual environment (e.g., `~/venvs/<project_name>`) outside the project's working directory to prevent corruption or accidental deletion.
  - [ ] **Create an Environment State File:** The `WorkflowState` should store the absolute path to the project's virtual environment's Python interpreter.
  - [ ] **Modify Command Execution:** All `run_command` calls that execute Python scripts or modules (`python3 -m...`, `pytest`, etc.) must be modified to use the explicit path from the state file (e.g., `/home/ubuntu/venvs/dw8/bin/python -m ...`). This eliminates any reliance on shell activation or `PATH` configuration.
  - [ ] **Update Project Setup:** The initial project setup workflow must include the creation of this environment and the installation of all dependencies as a primary, validated step.

---

### ID: REQ-DW8-002

- **Title:** Add a new `Rehearsal` state to the `WorkflowManager`'s state machine.
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** To combat cognitive fixation (OCB), a new `Rehearsal` state must be added to the state machine. This state will be triggered after repeated failures and will force a deep reflection and re-planning cycle.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, add `"Rehearsal"` to the `STAGES` list, before `"Deployer"`.
  - [ ] In `src/dw6/state_manager.py`, add an entry for `"Rehearsal"` in the `Governor.RULES` dictionary to allow for analysis and planning commands (e.g., `search_web`, `read_url_content`, `write_to_file`).
  - [ ] In `src/dw6/state_manager.py`, add a corresponding deliverable path for the `"Rehearsal"` stage in the `DELIVERABLE_PATHS` dictionary.

---

### ID: REQ-DW8-003

- **Title:** Implement the logic to trigger the `Rehearsal` state.
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The `WorkflowManager` must be able to detect consecutive failures and automatically transition the workflow into the `Rehearsal` state. This depends on `REQ-DW8-001`.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, define a `FAILURE_THRESHOLD` constant at the top of the file (e.g., `FAILURE_THRESHOLD = 3`).
  - [ ] In the `_handle_failure` method, after incrementing the counter, retrieve the new count.
  - [ ] Add a condition to check if the new count is greater than or equal to the `FAILURE_THRESHOLD`.
  - [ ] If the threshold is met, set `self.current_stage = "Rehearsal"`, save the state, and print a clear message indicating the transition to the `Rehearsal` state.

---

### ID: REQ-DW8-040

- **Title:** Authorize `approve` Command in Engineer Stage
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The `Engineer` stage currently lacks the permission to use the `approve` command, making it impossible to transition to the `Coder` stage. This is a critical workflow blockage.
- **SMRs:**
  - [x] In `src/dw6/state_manager.py`, add `"uv run python -m dw6.main approve"` to the `Governor.RULES` dictionary for the `"Engineer"` stage.

---

### ID: REQ-DW8-041

- **Title:** Correct Workflow Stage Progression
- **Status:** `Deployed`
- **Priority:** `Critical`
- **Details:** The workflow is incorrectly transitioning from the `Engineer` stage to the `Researcher` stage. The `Researcher` stage should not be part of the primary workflow cycle. The correct progression is `Engineer` -> `Coder`.
- **SMRs:**
  - [x] In `src/dw6/state_manager.py`, remove `"Researcher"` from the `STAGES` list to ensure the correct `Engineer` -> `Coder` transition.

---

### ID: REQ-DW8-042

- **Title:** Create Integration Test for Rehearsal State Transition
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** To ensure the reliability of the new `Rehearsal` state, a dedicated integration test must be created. This test will verify that the workflow correctly transitions to the `Rehearsal` state after the failure threshold is met.
- **SMRs:**
  - [ ] Create a new test file: `tests/test_rehearsal_integration.py`.
  - [ ] Implement a test case that simulates `FAILURE_THRESHOLD` consecutive failures.
  - [ ] Assert that the `CurrentStage` in the `.workflow_state` file is updated to `Rehearsal`.

---

### ID: REQ-DW8-043

- **Title:** Correct Test Setup for Rehearsal Integration Test
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The `test_rehearsal_integration.py` test is failing due to an `AttributeError`. The `WorkflowManager` instance under test is creating its own default `WorkflowState` object instead of using the one prepared in the test's `setUp` method. This causes a type mismatch on the `state_file` attribute.
- **SMRs:**
  - [ ] In the `setUp` method of `TestRehearsalIntegration`, refactor the initialization to directly inject the test's `WorkflowState` object into the `WorkflowManager` instance.

---

### ID: REQ-DW8-044

- **Title:** Configure Mock to Include `__name__` Attribute
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The rehearsal integration test is failing with an `AttributeError: __name__`. The `_get_failure_context` method requires the `__name__` attribute from the mocked `_validate_tests` function, but the default `MagicMock` does not have it.
- **SMRs:**
  - [ ] In `test_rehearsal_integration.py`, explicitly set the `__name__` attribute on the `mock_validate_tests` object to a string value (e.g., `'_validate_tests'`).

---

### ID: REQ-DW8-045

- **Title:** Fully Synchronize WorkflowManager State in Integration Test
- **Status:** `Deployed`
- **Priority:** `High`
- **Details:** The rehearsal integration test is failing because the `WorkflowManager` initializes its `current_stage` and `governor` from the default state file before the test can inject its own state. This causes an off-by-one error in the failure simulation.
- **SMRs:**
  - [ ] In `test_rehearsal_integration.py`, after injecting the test state object, explicitly re-initialize `self.manager.current_stage` and `self.manager.governor` to ensure they are synchronized with the test's state.

---

### ID: REQ-DW8-046

- **Title:** Correct `get_changes_since_last_commit` Method Signature
- **Status:** `In Progress`
- **Priority:** `High`
- **Details:** Approving the `Coder` stage fails with a `TypeError` because `git_handler.get_changes_since_last_commit` is called with a `commit_sha` argument, but its definition does not accept any parameters.
- **SMRs:**
  - [ ] Modify the signature of `get_changes_since_last_commit` in `src/dw6/git_handler.py` to accept a `commit_sha` argument.
  - [ ] Update the method's internal logic to use the provided `commit_sha` in the `git diff` command.

---

### ID: REQ-DW8-047

- **Title:** Correct Workflow Progression to Deployer Stage
- **Status:** `In Progress`
- **Priority:** `High`
- **Details:** After a successful `Validator` stage, the workflow incorrectly transitions to `Rehearsal` instead of `Deployer`. This is because `Rehearsal` is improperly included in the main `STAGES` list.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, remove `"Rehearsal"` from the `STAGES` list.
  - [ ] Manually reset the `CurrentStage` in `.workflow_state` back to `Validator` to allow for a correct re-approval.

---

### ID: REQ-DW8-048

- **Title:** Implement Protocol Evolution Sub-Workflow in Deployer Stage
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The `_validate_deployment` method is currently a placeholder and does not implement the required logic for deploying a new version of the DW protocol. It must be enhanced to check for the `is_protocol_update` flag and execute the full protocol evolution sub-workflow.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, modify `_validate_deployment` to check for `self.state.get('is_protocol_update')`.
  - [ ] Implement the logic to create a new versioned protocol directory (e.g., `/home/ubuntu/devs/dw/dw8`).
  - [ ] Implement the logic to generate a new versioned start script (e.g., `.windsurf/workflows/start-project-dw8.md`).
  - [ ] Implement the logic to generate a comprehensive `README.md` for the new protocol version.
  - [ ] Ensure all new artifacts are committed and pushed to the master Git repository.

---

### ID: REQ-DW8-049

- **Title:** Correct Regex for Protocol Version Parsing
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The `_execute_protocol_evolution` method fails because the regex `r'dw(\\d+)'` is incorrect for parsing the version number from the project name. The double backslash escapes the `d`, preventing a match.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, change the regex to `r'dw(\d+)'` to correctly capture the digits.

---

### ID: REQ-DW8-050

- **Title:** Debug Protocol Evolution Failure
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The `_execute_protocol_evolution` method fails with a cryptic error message. The exception handling must be enhanced to provide a full traceback to diagnose the root cause.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, modify the `except` block in `_execute_protocol_evolution` to print the exception type, details, and full traceback.

---

### ID: REQ-DW8-051

- **Title:** Revise Protocol Evolution Strategy to be Self-Contained
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The deployment fails with `InvalidGitRepositoryError` because the code incorrectly assumes `~/devs` is a Git repository. The new strategy will create all protocol artifacts *inside* the existing project repository to ensure they can be committed.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, modify `_execute_protocol_evolution` to create the new protocol directory relative to the project root.
  - [ ] The `start-project-dwX.md` script will also be created inside this new directory.
  - [ ] The `git.Repo` object will be initialized with the project root, not its parent.
  - [ ] The `git add` command will target the new subdirectory within the project.

---

### ID: REQ-DW8-052

- **Title:** Authorize `approve` Command in Rehearsal Stage
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The workflow is deadlocked in the `Rehearsal` stage because the `approve` command is not authorized by the `Governor`. The rules must be updated to allow `approve` as a valid exit command for this stage.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, add `uv run python -m dw6.main approve` to the `Rehearsal` stage's list of allowed command prefixes in `Governor.RULES`.

---

### ID: REQ-DW8-053

- **Title:** Implement Return Path from Rehearsal Stage
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The workflow fails when approving the `Rehearsal` stage because it's not in the main `STAGES` list. The logic must be updated to handle this special case by storing the stage of origin and returning to it.
- **SMRs:**
  - [ ] In `_handle_failure`, when transitioning to `Rehearsal`, save the current stage to a new `ReturnStage` variable in the state file.
  - [ ] In `_advance_stage`, check if the current stage is `Rehearsal`. If so, set the new stage to the `ReturnStage` value instead of using the `STAGES` list.

---

### ID: REQ-DW8-054

- **Title:** Manually Correct State to Exit Rehearsal Paradox
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The workflow is stuck in `Rehearsal` because the `ReturnStage` variable was not set when the state was entered. The `.workflow_state` file must be manually edited to add `ReturnStage=Deployer` to allow the new exit logic to function.
- **SMRs:**
  - [ ] Edit `.workflow_state` to add the `ReturnStage=Deployer` key-value pair.

---

### ID: REQ-DW8-055

- **Title:** Implement `delete` Method in `WorkflowState` Class
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The workflow fails with an `AttributeError` because the `_advance_stage` method calls `self.state.delete()`, which does not exist. The `WorkflowState` class must be enhanced with a method to remove keys from the state.
- **SMRs:**
  - [ ] In `src/dw6/state_manager.py`, add a `delete(self, key)` method to the `WorkflowState` class.

---

### ID: REQ-DW8-056

- **Title:** Fix `NameError` and `GitCommandError` in `git_handler`
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The deployment push fails due to two errors: a `NameError` because the `time` module is not imported, and a `GitCommandError` because the remote URL with the PAT is malformed. Both must be fixed in `src/dw6/git_handler.py`.
- **SMRs:**
  - [ ] Add `import time` to `src/dw6/git_handler.py`.
  - [ ] Correct the URL construction in the `get_remote_url_with_pat` method to prevent misinterpretation of the PAT.

---

### ID: REQ-DW8-057

- **Title:** Fix Persistent `GitCommandError` with Simplified URL Construction
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** The deployment push continues to fail with a URL rejection error, indicating the `urlparse` fix was ineffective. The `get_remote_url` method in `git_handler.py` must be rewritten using a simpler, direct string replacement to construct the authenticated URL.
- **SMRs:**
  - [ ] Replace the `urlparse`-based logic in `get_remote_url` with a direct string replacement.

---

### ID: REQ-DW8-001

- **Title:** Implement a persistent failure counter within the `WorkflowState`.
- **Status:** `In Progress`
- **Priority:** `Critical`
- **Details:** Create a mechanism to track consecutive failures for critical actions. This is the foundation for the `Rehearsal` state.
- **SMRs:**
  - [x] Engineer a technical specification for the failure counter.
  - [ ] Implement `_increment_failure_counter` helper method in `WorkflowManager`.
  - [ ] Implement `_reset_failure_counters` helper method in `WorkflowManager`.
  - [ ] Integrate counter logic into `_validate_deployment` and `_advance_stage`.

---

### ID: REQ-DW8-META-001

- **Title:** Implement `is_protocol_update` flag and management.
- **Status:** `Pending`
- **Priority:** `High`
- **Details:** Add a boolean flag to the `WorkflowState` to signify when a project is intended to evolve the DW protocol itself, triggering a special deployment sub-workflow.
- **SMRs:**
  - [ ] Add `is_protocol_update` to the `WorkflowState` JSON structure.
  - [ ] Modify the `dw6` CLI to allow setting this flag at project initiation.

---

### ID: REQ-DW8-META-003

- **Title:** Enhance `Deployer` stage to handle protocol evolution.
- **Status:** `Pending`
- **Priority:** `High`
- **Details:** The `_validate_deployment` method must be updated to check for the `is_protocol_update` flag and execute the protocol evolution sub-workflow.
- **SMRs:**
  - [ ] Add a check for the `is_protocol_update` flag at the beginning of `_validate_deployment`.
  - [ ] Implement the four functions for the sub-workflow: directory creation, script creation, documentation generation, and Git push.

---

### ID: REQ-GIT-REFACTOR-001

- **Title:** Refactor all git operations to use the GitHub MCP server.
- **Status:** `Halted`
- **Priority:** `Medium`
- **Details:** The current implementation uses a mix of `gitpython` and placeholder MCP functions. All git interactions (push, tag, etc.) must be fully migrated to use the `github-mcp-server` tools to overcome platform firewall restrictions and enable full automation.
- **SMRs:**
  - [ ] Implement the `mcp_push_files` function in `git_handler.py` using the `mcp5_push_files` tool.
  - [ ] Implement the `mcp_create_and_push_tag` function in `git_handler.py` using the new `mcp5_create_tag` tool (see REQ-DW8-010).
  - [ ] Replace all remaining `gitpython` calls in `state_manager.py` with the new `git_handler` functions.

---

### ID: REQ-DW8-008

- **Title:** Implement Automatic Batching for Large Git Pushes
- **Status:** `Pending`
- **Priority:** `High`
- **Details:** The `git_handler.mcp_push_files` function is currently a simple placeholder. It should be implemented with logic to handle an arbitrary number of files without failing due to API payload limits. When called, the function should check the number of files to be pushed. If the number exceeds a safe threshold (e.g., 5 files), it should automatically break the operation into a series of smaller, sequential commits, pushing each batch separately until all files are committed. This makes the push operation resilient and removes the burden of manual batching from the AI agent.
- **SMRs:**
  - [ ] Refactor `git_handler.mcp_push_files` to accept a list of file paths and a single commit message prefix.
  - [ ] Implement a loop within the function to iterate through the files in batches.
  - [ ] For each batch, call the `mcp5_push_files` tool with a modified commit message (e.g., "feat: My Feature (part 1/N)").
  - [ ] Add robust error handling to stop the process if any single batch fails.

---

### ID: REQ-DW8-009

- **Title:** Enhance MCP Error Handling with Agent-Guiding Diagnostics
- **Status:** `Pending`
- **Priority:** `Medium`
- **Details:** When an MCP tool fails, the returned error can be generic. We need to create a wrapper around critical tools (like `mcp5_push_files`) that can interpret known error patterns and provide actionable suggestions to the AI agent. This will accelerate debugging and help break fixation loops.
- **SMRs:**
  - [ ] Create a new error-handling module or class.
  - [ ] Implement a wrapper function for `mcp5_push_files`.
  - [ ] Inside the wrapper, catch the "generation exceeded max tokens limit" error specifically.
  - [ ] If that error is caught, raise a new, more descriptive exception, such as: "PushError: Commit payload is too large. Suggestion: Rerun the operation with a smaller number of files or use a function that supports automatic batching."

---

### ID: REQ-DW8-010

- **Title:** Add Git Tagging Capability to `github-mcp-server`
- **Status:** `Pending`
- **Priority:** `High`
- **Details:** The current `github-mcp-server` lacks the ability to create and push Git tags, which is a mandatory step in the `Deployer` stage. This prevents the full automation of the release process. A new tool, `mcp5_create_tag`, must be added to the server to create annotated tags via the GitHub API.
- **SMRs:**
  - [ ] Design the `mcp5_create_tag` tool, specifying its parameters and return value.
  - [ ] Implement the new tool in the `github-mcp-server` to make the necessary `POST` requests to the GitHub API.
  - [ ] Update `git_handler.mcp_create_and_push_tag` to use this new tool.

---

### ID: REQ-DW8-004

- **Title:** Define and implement the analytical tasks for the `Rehearsal` state.
- **Status:** `Pending`
- **Priority:** `Medium`
- **Details:** The `Rehearsal` state must guide the AI through a structured analysis of its failure, including reviewing logs, re-reading plans, and exploring alternative solutions.
- **SMRs:**
  - [ ] Define the specific prompts and tool calls the AI will use to analyze failures.
  - [ ] Implement the logic for the AI to propose at least two new alternative plans.

---

### ID: REQ-DW8-005

- **Title:** Implement the Escalation Protocol.
- **Status:** `Pending`
- **Priority:** `Low`
- **Details:** If the `Rehearsal` state fails, the system must automatically create a "Failed Requirement" ticket and reset the workflow to the `Engineer` stage for a full re-evaluation.
- **SMRs:**
  - [ ] Create a template for the "Failed Requirement" markdown file.
  - [ ] Implement the logic to generate this file.
  - [ ] Implement the function to reset the workflow state to `Engineer` and point it to the new failed requirement.

---

### ID: REQ-DW8-006

- **Title:** Develop a mechanism for "Spontaneous Reflection".
- **Status:** `Pending`
- **Priority:** `Low`
- **Details:** Implement a probabilistic check at stage transitions to ensure the AI's actions remain aligned with the high-level project goals.
- **SMRs:**
  - [ ] Add a probabilistic trigger to the `_advance_stage` method.
  - [ ] Define the "sanity check" prompt and logic.