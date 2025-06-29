# DW8: The AI-Centric Development Workflow

## 1. Vision: The Prism Protocol

The DW8 project is an advanced, AI-native software development workflow designed to overcome the limitations of its predecessor, DW6. The core vision, known as the **Prism Protocol**, is to create a development environment optimized for clarity, precision, and AI-driven automation. The system is built on the principle that a highly structured, transparent, and well-documented workflow allows an AI agent to operate with maximum efficiency and minimal ambiguity.

Our goal is to build a system where the AI can independently manage the entire development lifecycle—from requirement analysis to deployment—by interacting with a state machine governed by explicit, machine-readable rules and protocols.

## 2. Architecture: A Governor-Kernel Model

The DW8 system is built on a powerful and flexible **Governor-Kernel** architecture.

- **The Governor (`governor.py`):** The master controller and the single entry point for the entire workflow. It is responsible for initializing the environment, loading the system's state, and dispatching commands to the appropriate sub-system. It acts as a gatekeeper, ensuring that all operations adhere to the protocol.

- **The Workflow Kernel (`kernel.py`):** The engine of the workflow. It manages the state machine, transitioning between stages (`Engineer`, `Coder`, `Validator`, etc.) and executing the specific logic for each stage. The kernel is designed to be highly dynamic, loading its methods and capabilities from a structured directory, allowing for seamless evolution and extension of the protocol without core code changes.

- **The State Manager (`state_manager.py`):** The single source of truth for the system's state. It manages the `workflow_state.json` file, providing a robust interface for reading, writing, and persisting the workflow's current stage, requirement pointers, failure counters, and other critical data.

### Core Components:

- **Stage Modules (`src/dw6/workflow/`):** Each workflow stage (`engineer.py`, `coder.py`, etc.) is implemented as a separate module containing a class that defines the stage's specific logic and validation criteria.

- **Kernel Methods (`src/dw6/workflow/kr/`):** These are the atomic operations that the kernel can perform, such as advancing the stage, refreshing context, or handling failures. This modular design allows for easy maintenance and testing.

- **Event Ledger (`docs/EVENTS.json`):** A comprehensive, machine-readable ledger of all project requirements, bug reports, and refactoring tasks. This centralized JSON file is the primary input for the workflow, driving the development process.

- **Documentation (`docs/`):** All documentation is designed to be AI-native, using lightweight Markdown and structured JSON. Key documents include this `README.md`, the `API_REFERENCE.md`, and the `EVENTS.json` ledger.

## 3. The Workflow State Machine

The protocol is a state machine that guides development in a structured way. Each stage has a specific objective:

- **`Engineer`:** Define the problem, break it down into the smallest possible, verifiable requirements, and ensure the plan is sound.
- **`Researcher`:** (Optional) Explore different approaches, consult documentation, and create a detailed implementation plan.
- **`Coder`:** Write the code to implement the specific requirements. This stage is now protected by a validation check that requires a new Git commit before approval.
- **`Validator`:** Run the automated test suite (`pytest`) to ensure the new code works and has not introduced regressions.
- **`Deployer`:** Manages deployment and protocol synchronization, ensuring the master workflow is always up-to-date.
- **`Rehearsal`:** A special "time-out" state triggered by repeated failures, forcing a deep reflection on the root cause.

## 4. Key CLI Commands

The workflow is managed through a set of simple CLI commands:

- `uv run dw6 status`: Shows the current state of the workflow.
- `uv run dw6 approve`: Approves the current stage's exit criteria and advances to the next stage.
- `uv run dw6 new`: Guides the user through creating a new requirement.

## 5. Failure Handling

The protocol is designed to be resilient:

- **Failure Counters:** The system tracks consecutive failures for each stage and requirement.
- **The Rehearsal State:** When a failure threshold is reached, the workflow automatically enters the `Rehearsal` state to force a strategic reassessment.
# DW8 Boot Protocol (BOOT_PROTOCOL.md)

## 1. Objective

This document defines the formal, sequential process for the DW8-OS system startup. The protocol ensures that the system initializes in a consistent, predictable, and reliable state every time it is launched.

## 2. Trigger

The boot sequence is triggered by the execution of the main CLI entry point, for example:
```bash
/home/ubuntu/devs/dw7_protocol_test_bed/.venv/bin/python -m dw6.main status
```

## 3. Core Initialization Sequence

The startup process follows a strict order to ensure all components are loaded and available before the system attempts to perform any actions.

### Step 1: Load Workflow State

The first action is to read the `.workflow_state` file. This file is the single source of truth for the system's current operational context.

- **Action:** The `WorkflowState` class is instantiated.
- **Result:** The system loads critical state information, including `CurrentStage`, `RequirementPointer`, and any `FailureCounters`.

### Step 2: Initialize the Workflow Kernel

With the state loaded, the `WorkflowKernel` is initialized. The kernel is the heart of the OS, responsible for managing core logic and event processing.

- **Action:** The `WorkflowKernel` class is instantiated, receiving the `WorkflowState` object.
- **Result:** During its initialization, the kernel immediately calls its `load_current_event_details()` method. It uses the `RequirementPointer` from the state to read the `data/pending_events.json` file and load the full details of the currently active requirement into memory. This ensures the system always knows what it's working on.

### Step 3: Initialize the Workflow Manager

The `WorkflowManager` acts as the high-level controller, orchestrating the different stages of the workflow.

- **Action:** The `WorkflowManager` class is instantiated, receiving the `WorkflowState` object.
- **Result:** The manager reads the `CurrentStage` from the state and dynamically loads the corresponding stage module (e.g., `EngineerStage`, `CoderStage`). This prepares the system to execute the logic specific to the current stage.

## 4. System Ready

Once these three steps are complete, the DW8-OS is considered fully booted and is ready to accept and process user commands via the CLI. The system is now in a known, stable state.
# PROTOCOL: Context Awareness Hazard

**WARNING: This protocol addresses a catastrophic failure mode for the autonomous system.**

## 1. The Hazard: Catastrophic Context Decay

The AI agent has a limited context window. Over long operational cycles, it is guaranteed to suffer from **context decay** (amnesia), forgetting critical project goals, architectural principles, and established protocols. This failure mode leads to redundant work, logical errors, and deviation from the strategic objectives, resulting in mission failure.

## 2. The Mandate: Proactive Documentation Review

To mitigate this hazard, the AI agent is **mandated** to treat the project's documentation as its external, persistent memory. The primary source of truth is the master guide:

*   `context/README_FIRST.md`

When faced with uncertainty, repeated errors, or the start of a new, complex task, the AI **must** consult this document and its referenced protocols before proceeding.

## 3. The Implementation: The System Reminder

To enforce this mandate, the `WorkflowManager` will issue a hardcoded reminder to the AI at the beginning of every significant work cycle (e.g., when the `status` command is invoked). This reminder serves as a non-negotiable directive to refresh its context.

## 4. Expected AI Behavior

The AI agent must acknowledge this protocol and integrate it into its core operational loop. It must not dismiss the system reminder and should demonstrate evidence of using the documentation to guide its actions.

## 5. Addendum: Focus on Substance Over Syntax
To conserve focus and tokens, the AI agent is explicitly forbidden from correcting minor, non-functional syntax or linting errors in Markdown (`.md`) files. The readability and meaning of the documentation are paramount; stylistic perfection is not. This is a directive to prevent low-value, obsessive-compulsive corrections.
# DW8 Context Management Protocol

## 1. Objective

This protocol defines the formal strategy for managing the AI's context window. Its primary purpose is to combat context decay by ensuring the AI regularly receives a concise, high-level summary of the project's goals and operating procedures. This keeps the AI aligned with the mission and prevents it from losing track of the bigger picture.

## 2. Mechanism: Mandatory Context Refresh

The core of this protocol is a mandatory, automated context refresh. This is not an optional step but a fundamental part of the workflow loop, managed by the `WorkflowKernel`.

## 3. Trigger

The context refresh is automatically triggered by the `WorkflowKernel` upon the successful completion of the `Validator` stage for any given requirement. 

This timing is deliberate:
- It marks the end of a complete work cycle.
- It occurs just before the system transitions to a new requirement and resets to the `Engineer` stage.
- It provides a natural and efficient point to reload context without interrupting an active work stream.

## 4. Content of the Refresh

The context refresh payload is designed to be concise yet comprehensive. It includes two key components:

1.  **The Next Active Event:** The full details of the next requirement in the pending queue (e.g., `REQ-DW8-OS-012`). This immediately focuses the AI on the next task.

2.  **The AI Protocol Tutorial:** A high-level summary of the core DW8 workflow, its stages, key CLI commands, critical files, and failure handling procedures. This serves as a quick-reference guide to reinforce the fundamental operating principles.

By combining the immediate next task with the overarching project context, this protocol ensures the AI is always grounded and working with the most relevant information.
# PROTOCOL: Documentation Integrity

## 1. The Principle
A feature is not considered complete until its corresponding documentation is updated. Code and documentation must always be synchronized to prevent documentation drift, which is a critical failure mode for a protocol-driven system.

## 2. The Mechanism: The 'affected_documents' List
To enforce this principle, all requirement definitions (in the `events/` directory) must include an `affected_documents` key. This key will hold a list of strings, where each string is the absolute path to a documentation file that must be created or updated as part of the requirement's implementation.

## 3. The Enforcement
- **Planning:** During the `Engineer` stage, the `affected_documents` list must be populated.
- **Implementation:** During the `Coder` stage, the AI agent's work is not complete until it has submitted changes for both the source code and all files listed in `affected_documents`.
- **Validation:** During approval, the human operator can use this list as a checklist to verify that documentation has been properly updated.
# DW8 Protocol: Code Granularity

## 1. Principle

To improve the reliability of AI-driven code modifications, large source code files will be refactored into a more granular "interface/implementation" structure. This ensures that the AI agent's context is always focused and accurate when performing file edits, minimizing errors caused by context drift.

## 2. The Trigger

This refactoring protocol should be applied to any source code file that exceeds **150 lines** of code.

## 3. The Refactoring Procedure

When a file is refactored, the following steps must be taken:

1. **Create Implementation Directory:** A new directory is created alongside the original file. The directory name is a concise, deterministic abbreviation of the original filename (e.g., `deployer.py` -> `dp/`).
2. **Extract Methods:** Each function or class method from the original file is moved into its own separate Python file inside the new implementation directory. The filename is an abbreviation of the function name (e.g., `_execute_protocol_evolution` -> `exec_proto_evo.py`).
3. **Create Interface File:** The original file becomes the "interface." Its contents are replaced with logic that dynamically imports all the functions/methods from the implementation directory and attaches them to the appropriate class or module scope.

## 4. Naming Convention

- **Directories:** A 2-3 letter abbreviation of the source file. E.g., `deployer.py` -> `dp/`.
- **Files:** A snake_case abbreviation of the function name. E.g., `_check_if_project_is_complete` -> `chk_proj_cpl.py`.
# DW8 Protocol: The Deployer Stage

This document formalizes the complete vision for the `Deployer` stage, transforming it from a placeholder into a robust, automated deployment and versioning engine. It addresses two critical scenarios: standard project deployment and protocol evolution deployment.

## 1. Core Principle

The `Deployer` stage is the final step in every development cycle. Its primary responsibility is to ensure that all work is durably stored, versioned, and, where applicable, officially released. It must handle both the project's own codebase and the evolution of the DW protocol itself, using the `github-mcp-server` to avoid manual authentication and automate all Git operations.

## 2. Scenario A: Standard Project Deployment

This is the default behavior for any project that is **not** updating the DW protocol itself.

1. **End-of-Cycle Push:** At the conclusion of every development cycle (i.e., when a requirement is moved to `Deployed`), the `Deployer` will automatically commit and push all changes in the project directory to its designated Git repository.
2. **Repository Creation:** If the target repository does not exist, the `Deployer` will use the `github-mcp-server` to create it automatically.
3. **Versioning:** Each end-of-cycle push will be versioned using a Git tag (e.g., `v1.1`, `v1.2`, etc.) to create a clear history of completed requirements.
4. **Final Documentation:** Upon completion of the *entire project* (all requirements are `Deployed`), the `Deployer` will generate a comprehensive `README.md`. This file will include an overview of the project, installation instructions, usage guides, and API/function documentation. This `README.md` will be included in the final push.

## 3. Scenario B: Protocol Evolution Deployment

This scenario is triggered when the `is_protocol_update` flag is `true`.

1. **Dual-Push Mandate:** The `Deployer` must perform **two** distinct push operations at the end of every cycle:
    - **Push 1 (Test Bed):** Commit and push the changes from the current project directory (e.g., `dw7_protocol_test_bed`) to its own repository, following the standard versioning procedure.
    - **Push 2 (Official Protocol):** Commit and push the updated workflow logic to the official `windsurf-development-workflow` repository. This ensures that valuable improvements to the protocol are never lost and are versioned centrally.
2. **Protocol Synchronization:** Before pushing to the official repository, the `Deployer` must first copy the finalized source code (e.g., from `src/dw6`) to the official versioned protocol directory (e.g., `/home/ubuntu/devs/dw/dw8`).

## 4. Configuration and Credential Management

To power this automation, the `Deployer` will rely on a new configuration system:

1. **Credential Setup:** On first use with a new user/project, the workflow will prompt for Git credentials. These credentials will be stored securely in a local `.env` file.
2. **MCP Integration:** The user will be asked for permission to configure the `github-mcp-server` with these credentials, enabling seamless, non-interactive Git operations in the future.
3. **Configuration File:** A new file, `docs/DEPLOYER_CONFIGURATION.md`, will be created to store all necessary paths and URLs, such as the official protocol directory, the official repository URL, and the project-specific repository URL. The `DeployerStage` will read this file to get its operational parameters.
# DW8 Protocol: Dynamic Requirement Management

This document formalizes the standard operating procedure for handling the creation of new Meta-Requirements (MRs) during an active development workflow. This protocol ensures that new ideas, improvements, or bug fixes are captured, prioritized, and integrated without losing momentum.

## 1. Principle

The DW8 workflow must be agile and responsive to new information. This protocol provides a structured way to pause the current task, formalize a new requirement, and intelligently resume work based on the most current priorities.

## 2. The Trigger

This sub-workflow can be triggered at any time by:

- A direct user interruption to suggest a new feature, improvement, or bug fix.
- An AI-initiated `Rehearsal` or `Spontaneous Reflection` that uncovers a deeper issue requiring a new MR.
- The conclusion of a brainstorming session.

## 3. The Procedure

Upon triggering, the AI agent will execute the following steps:

1.  **Acknowledge and Pause:** Announce the initiation of the Dynamic Requirement Protocol and pause the current task.
2.  **Formalize the Requirement:** Create a new, detailed MR file in the `docs/reqs/` directory.
    - Assign a new, sequential ID (e.g., `REQ-DW8-XXX`).
    - Define the Title, Status (defaulting to `Pending`), Priority (`Critical`, `High`, `Medium`, `Low`), Details, and a checklist of Sub-Meta-Requirements (SMRs).
3.  **Update the Master Index:** Add a reference to the new MR file in `docs/PROJECT_REQUIREMENTS.md`.
4.  **Execute the Rescheduling Protocol:** This is the most critical step. Re-read the entire, updated `docs/PROJECT_REQUIREMENTS.md` file and re-sort the list of all `Pending` requirements according to their priority (`Critical` first, then `High`, `Medium`, `Low`). This ensures the workflow's focus is always on the most important task.
5.  **Announce and Resume:** Announce the new, top-priority task and resume the workflow by beginning work on that requirement.
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
# DW8 Protocol: Robust Command Output Handling

## 1. Principle

To ensure the AI agent can make accurate, evidence-based decisions, all critical shell commands must be executed in a way that guarantees the capture of their complete, untruncated output. This protocol formalizes the procedure for achieving this, preventing the misdiagnosis of failures due to incomplete information.

## 2. The Trigger

This protocol must be used whenever the outcome of a shell command is critical for a validation step or a key decision. This includes, but is not limited to:

- Running test suites (e.g., `pytest`).
- Complex build or compilation scripts.
- Any command whose output needs to be parsed or checked for specific results.

## 3. The Procedure

The agent will execute the following three-step process:

1. **Execute and Redirect:** The command will be executed using the `run_command` tool. The command string must include redirection of both `stdout` and `stderr` to a temporary log file. For example: `my_critical_command > command_output.log 2>&1`.
2. **Read Full Output:** Immediately after the command completes, the agent will use the `mcp3_read_file` tool to read the entire contents of the temporary log file. This provides a complete and untruncated record of the command's execution.
3. **Analyze and Clean Up:** The agent will analyze the captured output to determine the outcome. After the analysis is complete, the agent should delete the temporary log file to maintain a clean working directory.
# DW8 Environment Management Protocol

## 1. The Problem: Fragile Environment Context

A persistent failure point in the DW8 system is the loss of the Python virtual environment (`venv`) context between sessions and stage transitions. This leads to errors, delays, and manual re-installations. The root cause is the lack of a persistent mechanism to store the path to the correct Python executable.

## 2. The Solution: Persistent State Management

This protocol establishes a robust, file-based state management system to ensure the environment context is never lost. The core of this system is the `.workflow_state` file.

## 3. The `.workflow_state` File

- **Purpose:** To act as the single, persistent source of truth for the workflow's state.
- **Location:** Project root (`/home/ubuntu/devs/dw7_protocol_test_bed/.workflow_state`).
- **Format:** JSON.
- **Key Fields:**
  - `PythonExecutablePath`: The absolute path to the Python executable within the project's `.venv`.
  - `CurrentStage`: The current stage of the workflow.
  - `RequirementPointer`: The ID of the active requirement.
  - `FailureCounters`: A dictionary of failure counters for critical operations.

## 4. The `WorkflowState` Class

A new class, `WorkflowState`, will be implemented in `state_manager.py`. Its sole responsibility is to manage the `.workflow_state` file.

- **Responsibilities:**
  - Reading the state file on initialization.
  - Writing updates to the state file.
  - Providing a clean API (`get(key)`, `set(key, value)`) for other parts of the system to access state information without directly interacting with the file.

## 5. The Setup and Enforcement Loop

1.  **Setup:** The environment setup script (`scripts/setup.sh` or similar) will be modified. After creating the `venv`, it will execute a Python script (`dw6.setup.initialize_state`).

2.  **Initialization:** The `initialize_state` script will:
    - Capture the absolute path to `/.venv/bin/python`.
    - Instantiate the `WorkflowState` class.
    - Call `WorkflowState.set('PythonExecutablePath', path)` to create and populate the `.workflow_state` file.

3.  **Enforcement:** The `WorkflowManager` and `WorkflowKernel` will be refactored to:
    - Load the state using the `WorkflowState` class upon instantiation.
    - Retrieve the `PythonExecutablePath` from the state.
    - Use this specific path for all subsequent shell commands (e.g., running `pytest`), thus guaranteeing the correct environment is always used.
# DW8 Git Workflow Protocol

## 1. The Problem: Ad-Hoc Git Usage

The current Git integration is a collection of utility functions rather than a coherent, automated workflow. It lacks a formal branching strategy, leading to all work being done directly on the main branch. This is fragile and does not scale.

## 2. The Solution: Automated Feature Branch Workflow

This protocol implements a strict, automated feature branch workflow. Every new piece of work is developed in isolation on a dedicated branch, ensuring the `main` branch always remains stable and deployable.

## 3. The Protocol Steps

### Step 1: Branch Creation (Engineer Stage)

- **Trigger:** The start of the `Engineer` stage for any new requirement (e.g., `REQ-DW8-019`).
- **Action:** The `Governor` will automatically create a new feature branch.
- **Naming Convention:** The branch will be named `feature/[Requirement-ID]`. For example: `feature/REQ-DW8-019`.
- **Process:** All subsequent work for this requirement (`Coder`, `Validator`) **must** be done on this branch.

### Step 2: Committing (Coder Stage)

- **Standard:** All commit messages **must** follow the **Conventional Commits v1.0.0** specification.
- **Examples:**
  - `feat(kernel): Add new method for event processing`
  - `fix(cli): Correct argument parsing for 'new' command`
  - `docs(protocol): Update REHEARSAL_PROTOCOL.md`
- **Enforcement:** The `Governor` will validate the commit message format before allowing a commit.

### Step 3: Merging (Deployer Stage)

- **Trigger:** Successful completion of the `Validator` stage on the feature branch.
- **Action:** The `Deployer` stage is responsible for merging the feature branch back into `main`.
- **Merge Strategy:** The merge **must** be a non-fast-forward merge to preserve the context of the feature branch in the Git history.
  - `git merge --no-ff feature/REQ-DW8-019 -m "Merge feature 'REQ-DW8-019'"`

### Step 4: Cleanup (Deployer Stage)

- **Trigger:** A successful merge into `main`.
- **Action:** The `Deployer` will automatically delete the local and remote feature branch to keep the repository clean.
  - `git branch -d feature/REQ-DW8-019`
  - `git push origin --delete feature/REQ-DW8-019`

## 4. Implementation Notes

- The `git_handler.py` module will need to be significantly refactored to implement these automated steps.
- The `Governor` will be enhanced to enforce branch and commit message rules.
# DW8 Rehearsal Protocol (The Interrupt Handler)

## 1. Concept: Rehearsal as a System Interrupt

In the DW8-OS paradigm, the `Rehearsal` stage is not a standard step in the workflow. Instead, it functions as a critical **system interrupt handler**. Its purpose is to pause the normal execution flow to handle a specific type of fault: repeated, unrecoverable errors in any other stage.

This reframes the stage from a simple "time-out" to a formal, hardware-like interrupt, making the system's failure response more robust and predictable.

## 2. The Interrupt Trigger

The `Rehearsal` interrupt is triggered exclusively by the `WorkflowKernel`'s failure handling logic.

- **Condition:** A stage's failure counter (e.g., `Validator.pytest` or `Coder.default`) exceeds the system-defined `FAILURE_THRESHOLD`.
- **Action:** The Kernel immediately halts the current operation and initiates the interrupt sequence.

## 3. The Kernel's Role: The Interrupt Controller

When the interrupt is triggered, the `WorkflowKernel` performs the following actions, analogous to a CPU's interrupt controller:

1.  **Preserve Context:** The Kernel saves the name of the stage that failed by writing it to the `PreviousStage` key in the `.workflow_state` file. This is equivalent to pushing the current instruction pointer to the stack.

2.  **Load the Interrupt Handler:** The Kernel sets the `CurrentStage` to `Rehearsal`.

3.  **Vector to Handler:** The `WorkflowManager` detects the stage change and loads the `RehearsalStage` module, effectively passing control to the interrupt service routine.

## 4. The `RehearsalStage`: The Interrupt Service Routine

The `RehearsalStage` module contains the logic for handling the fault. Its responsibilities are strictly defined:

1.  **Analyze Fault Context:** The stage must first analyze the reason for the failure, using the `PreviousStage` value and system logs to understand what went wrong.

2.  **Re-evaluate the Plan:** It must re-read the active requirement and all relevant protocol documents to ensure its new plan is aligned with the project's goals.

3.  **Formulate a Recovery Plan:** The primary output of this stage is a new, detailed plan for overcoming the failure. This plan **must** include at least two distinct alternative solutions.

4.  **Request Approval:** The plan is presented for approval. The stage cannot exit until a valid recovery plan is approved.

## 5. Exiting the Interrupt

Once the recovery plan is approved, the `WorkflowKernel` executes the return from interrupt (`RTI`) sequence:

1.  **Restore Context:** The Kernel reads the `PreviousStage` value from the state file and sets it as the `CurrentStage` again, effectively popping the old instruction pointer off the stack.

2.  **Retry Operation:** The system is now back in the stage where it originally failed, but it is now equipped with a new, approved plan to retry the operation.
# DW8 Release Protocol

## 1. The Problem: No Formal Release Process

Currently, there is no formal process for versioning or releasing the software. This makes it difficult to track changes, manage dependencies, or roll back to stable versions. Releases are an implicit concept, not an explicit, automated action.

## 2. The Solution: Automated Semantic Versioning

This protocol implements a fully automated release process based on **Semantic Versioning 2.0.0**. It leverages the commit messages generated by the `GIT_WORKFLOW_PROTOCOL.md` to automatically determine version numbers and create formal releases.

## 3. The Protocol Steps

### Step 1: Analyze Commits (Deployer Stage)

- **Trigger:** A successful `--no-ff` merge into the `main` branch.
- **Action:** The `Deployer` will inspect all commit messages that were part of the merged feature branch.

### Step 2: Determine Next Version (Deployer Stage)

- **Logic:** The `Deployer` will apply the following rules based on the Conventional Commits standard:
  - If any commit message contains `BREAKING CHANGE:` in the footer, the version will receive a **MAJOR** bump (e.g., `1.2.3` -> `2.0.0`).
  - If any commit message contains a `feat:` type, the version will receive a **MINOR** bump (e.g., `1.2.3` -> `1.3.0`).
  - If all commit messages are of other types (`fix:`, `docs:`, `refactor:`, etc.), the version will receive a **PATCH** bump (e.g., `1.2.3` -> `1.2.4`).

### Step 3: Create Tag (Deployer Stage)

- **Action:** Once the new version number is determined, the `Deployer` will create a new, annotated Git tag.
- **Naming Convention:** `v[Major].[Minor].[Patch]`, for example: `v1.3.0`.
- **Command:** `git tag -a v1.3.0 -m "Release v1.3.0"`

### Step 4: Push Tag (Deployer Stage)

- **Action:** The `Deployer` will push the new tag to the remote repository, creating a formal, immutable release point.
- **Command:** `git push origin v1.3.0`

## 4. Implementation Notes

- This protocol requires a tool (or a new function in `git_handler.py`) that can parse Git history, identify the last tag, and analyze commit messages to determine the next semantic version.
- The `Deployer` stage logic will be significantly enhanced to orchestrate this release process.
# DW8 Workflow Adherence Protocol

## 1. The Problem: "Free as a Bird" Behavior

It has been observed that the AI agent can sometimes operate outside the strict boundaries of the prescribed DW8 workflow. This behavior undermines the core principle of a structured, predictable, and robust development process. This protocol is designed to eliminate this vulnerability.

## 2. The Solution: Stricter Governor Gates

The solution is to enhance the `Governor`'s role from a simple stage-exit validator to an **active, in-stage supervisor**. The `Governor` will now enforce a set of rules that define which actions are permissible within each stage of the workflow.

## 3. Mechanism: Pre-Execution Validation

Before executing any potentially stage-violating tool or command (e.g., `edit_file`, `run_command`), the `WorkflowManager` will consult the `Governor`. The `Governor` will then check the proposed action against a ruleset for the `CurrentStage`.

If the action is permitted, it is executed. If it is forbidden, the action is blocked, and the `Governor` will issue a formal warning, forcing the AI to choose a protocol-compliant action instead.

## 4. Stage-Specific Ruleset

This section defines the initial set of rules for each stage. This list can be expanded as the protocol matures.

### `Engineer` Stage
- **Permitted:** Reading/listing files (`view_file_outline`, `ls`), creating documentation (`write_to_file` in `docs/`).
- **Forbidden:** Editing application source code, running tests, running deployment scripts.

### `Coder` Stage
- **Permitted:** Editing and creating source code files (`edit_file`, `write_to_file` in `src/`).
- **Forbidden:** Running the full test suite (this is the `Validator`'s job), running deployment scripts.

### `Validator` Stage
- **Permitted:** Running the test suite (`pytest`).
- **Forbidden:** Editing any files.

### `Deployer` Stage
- **Permitted:** Running deployment scripts, `git` commands.
- **Forbidden:** Editing application source code.

## 5. Implementation Note

This protocol will require modifying the `WorkflowManager` to call a new validation method on the `Governor` before executing tool calls. The `Governor` will need to be enhanced with the logic to implement these stage-based rules.
# PROTOCOL: Workflow Operational Modes

## 1. The Principle
To ensure disciplined development, the workflow operates in distinct modes that separate high-level investigation and planning from low-level implementation. This prevents premature coding and ensures all work is grounded in a well-defined strategy.

## 2. Mode Definitions

*   **Sherlock Mode (Investigation):**
    *   **Purpose:** To investigate a problem, design a solution, and produce a set of granular, actionable requirements.
    *   **Allowed Stages:** `Engineer`, `Researcher`.
    *   **Forbidden Actions:** No code implementation (`Coder`), testing (`Validator`), or deployment (`Deployer`) is permitted. The output of this mode is a set of new requirement files in the `events/` directory.

*   **Execution Mode (Implementation):**
    *   **Purpose:** To implement, test, and deploy a solution based on a single, pre-existing requirement from the `events/` directory.
    *   **Allowed Stages:** `Coder`, `Validator`, `Deployer`.

## 3. Enforcement
The system state (`data/workflow_state.json`) must track the `CurrentMode`. The `Governor` must enforce the allowed stages and actions based on the active mode.
