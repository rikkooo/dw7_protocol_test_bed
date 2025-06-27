# Technical Specification for REQ-DW8-011: Robust and Persistent Virtual Environment Management

## 1. Overview

The previous development cycle was plagued by persistent, difficult-to-diagnose errors stemming from an inconsistent and unreliable Python virtual environment. The AI agent repeatedly failed to use the correct, activated environment, leading to `AttributeError`, `ModuleNotFound`, and incorrect script execution. This cognitive fixation on a broken environment highlights a critical flaw in the DW protocol: the environment is treated as an implicit, transient dependency rather than a core, stateful component of the workflow.

This document outlines the plan to fix this by making virtual environment management an explicit, robust, and persistent part of the DW8 protocol.

## 2. Proposed Solution

We will address this by implementing the four Sub-Meta-Requirements (SMRs) of `REQ-DW8-011`. The core idea is to create a standardized, external virtual environment at the beginning of a project, store the absolute path to its Python executable in the workflow's state file, and use that explicit path for all subsequent Python-related commands.

## 3. Implementation Details

### SMR-1: Standardize Environment Location & SMR-4: Update Project Setup

These two SMRs will be implemented together by modifying the project's startup process. The current test bed does not have a formal start script, so we will modify the `WorkflowManager` to simulate this process. In a real DW8 implementation, this logic would live in a `/start-project-dw8.md` workflow.

**File to Modify:** `src/dw6/state_manager.py`

1. **Modify `WorkflowState.initialize_state()`:**
   - This method will be enhanced to perform a one-time setup if the environment is not already configured.
   - It will define a standard venv path: `~/venvs/<project_name>/` (e.g., `/home/ubuntu/venvs/dw7_protocol_test_bed/`).
   - It will check if this directory exists. If not, it will execute the following shell commands:
     - `mkdir -p ~/venvs/`
     - `python3 -m venv ~/venvs/<project_name>`
     - `~/venvs/<project_name>/bin/python -m pip install -e .`

### SMR-2: Persist Environment Path in State

**File to Modify:** `src/dw6/state_manager.py`

1. **Modify `WorkflowState.initialize_state()`:**
   - After the one-time setup, the method will calculate the absolute path to the Python executable (e.g., `/home/ubuntu/venvs/dw7_protocol_test_bed/bin/python`).
   - It will add a new key to the state data: `PythonExecutablePath`.
   - The initial `workflow_state.txt` will now contain this key, making the environment's location a persistent part of the project state.

### SMR-3: Modify Command Execution

This SMR requires using the newly persisted path for all Python command execution. We will implement a concrete example of this pattern.

**File to Modify:** `src/dw6/state_manager.py`

1. **Modify `WorkflowManager._validate_tests()`:**
   - The method currently calls `subprocess.run(["python", "-m", "pytest"], ...)`.
   - It will be updated to first retrieve the `PythonExecutablePath` from the `self.state` object.
   - The `subprocess.run` call will be changed to `subprocess.run([python_executable_path, "-m", "pytest"], ...)`, where `python_executable_path` is the value retrieved from the state.

## 4. Testing Strategy

We will create a new test file to verify the correctness of these changes.

**New File:** `tests/test_environment_management.py`

1. **`test_state_initialization_creates_env_and_persists_path`:**
   - This test will patch `os.path.exists`, `subprocess.run`, and the `open` built-in.
   - It will instantiate `WorkflowState` and assert that the setup commands (`mkdir`, `venv`, `pip install`) are called in the correct order when the environment does not exist.
   - It will verify that the final state data written to the file contains the correct `PythonExecutablePath`.

2. **`test_validate_tests_uses_persistent_python_path`:**
   - This test will patch `subprocess.run`.
   - It will create a `WorkflowManager` instance, ensuring its state has a `PythonExecutablePath`.
   - It will call `_validate_tests()` and assert that `subprocess.run` was called with a command list starting with the correct, absolute path to the Python executable.

## 5. Deliverables

- Modified `src/dw6/state_manager.py`
- New test file `tests/test_environment_management.py`
