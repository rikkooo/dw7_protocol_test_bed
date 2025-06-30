# DW8 Code Atlas (API Reference)

This document is the single source of truth for the DW8 project's API. It is auto-generated from the source code's docstrings.

---
## Module: `dw6/augmenter.py`

### `class PromptAugmenter`
> Augments user prompts with context from the MCP server.

#### `def augment_prompt(self, original_prompt)`
> Fetches context and prepends it to the prompt.

---
## Module: `dw6/boot.py`

### `def ensure_environment()`
> Ensures that the project's virtual environment is set up correctly.

This function is idempotent. It checks for the existence of the virtual
environment and the installation of dependencies, and only performs setup
actions if they are needed.

---
## Module: `dw6/cli.py`

### `def main()`
> No docstring available.

---
## Module: `dw6/config.py`

---
## Module: `dw6/git_handler.py`

### `def add_commit_files(files, message)`
> Adds and commits a list of files.

### `def check_for_workflow_changes(repo: git.repo.base.Repo)`
> Checks if any files in the src/dw6/ directory have changed since the last cycle.

### `def commit_and_push_deliverable(file_path, stage_name, requirement_id)`
> Commits and pushes a deliverable file.

### `def get_changes_since_last_commit(commit_sha)`
> Gets the changed files and diff since the last saved commit.

### `def get_last_commit_sha()`
> Reads the last saved commit SHA from the Coder stage.

### `def get_latest_commit_hash(repo: git.repo.base.Repo = None)`
> Gets the hash of the latest commit.

### `def get_local_tags_for_commit(commit_hash, repo: git.repo.base.Repo = None)`
> Gets all local tags pointing to a specific commit.

### `def get_project_root() -> pathlib.Path`
> Returns the project root directory.

### `def get_repo() -> git.repo.base.Repo`
> Initializes and returns the git.Repo object.

### `def get_repo_info_from_remote_url(remote_url: str)`
> Extracts the repository owner and name from the remote URL.

### `def get_repo_owner_and_name()`
> Gets the repository owner and name from the remote URL.

### `def is_push_required(repo: git.repo.base.Repo = None)`
> Checks if the local branch is ahead of the remote branch.

### `def load_github_token(repo_path=None)`
> Loads the GitHub token from the .env file, prompting the user if not found.

### `def mcp_create_and_push_tag(tag_name, commit_sha, message='')`
> Creates an annotated tag for a specific commit and pushes it using the GitHub MCP server.
This function will be implemented by the agent using two calls to mcp2_fetch_json.

### `def mcp_push_files(commit_message, file_paths, branch='main')`
> Commits and pushes a list of files to the remote repository using the GitHub MCP server.
This function will be implemented by the agent using the mcp5_push_files tool.

### `def push_to_remote(repo=None, tags=False)`
> Pushes the current branch and optionally tags to the remote repository.

### `def save_current_commit_sha()`
> Saves the current commit SHA to a file for the Coder stage.

### `def save_github_token(token, env_path)`
> Saves the GitHub token to the .env file.

---
## Module: `dw6/governor.py`

### `class Governor`
> The master controller and protocol enforcer for the DW8 system.

The Governor acts as the primary interface between the user (the Principal)
and the AI's workflow engine (the Kernel). It is responsible for initializing
the system, enforcing protocol rules, handling user commands like 'approve',
and ensuring that the system state remains consistent.

While the Kernel manages the internal state machine, the Governor provides
the command-and-control layer that surrounds it.

Attributes:
    start_path (str, optional): The initial path from which the Governor
        is invoked. Used for context discovery.

#### `def approve_stage(self)`
> Approves the current stage and transitions to the next.

Note:
    This is currently a placeholder for future validation and state
    transition logic.

#### `def start_session(self, requirement_id: str)`
> Starts a new work session for a given requirement.

Note:
    This is currently a placeholder for future state transition logic.

Args:
    requirement_id (str): The unique identifier for the requirement
        to begin work on.

#### `def governor_authorize(self, command: str)` (Dynamically Loaded)
> Authorizes or denies a command based on the current workflow stage.

This function acts as the central gatekeeper for command execution, enforcing
the principle that only certain commands are permissible in specific stages.

It operates by:
1.  Identifying the current workflow stage (e.g., 'Engineer', 'Coder').
2.  Looking up the list of allowed command prefixes for that stage in the
    `RULES` class attribute.
3.  Checking if the given `command` string starts with any of the authorized
    prefixes.

If the command is not authorized, it prints a denial message to standard
error and returns False, preventing the command from being executed.

Args:
    self (Governor): The instance of the Governor.
    command (str): The command string to be authorized.

Returns:
    bool: True if the command is authorized, False otherwise.

Side Effects:
    - Prints an error message to `sys.stderr` if authorization fails.

---
## Module: `dw6/setup.py`

### `def create_venv(project_dir)`
> Creates a Python virtual environment.

### `def install_dependencies(project_dir)`
> Installs project dependencies from pyproject.toml.

### `def main()`
> Main function to set up the project environment.

### `def run_command(command, cwd=None)`
> Runs a command and exits if it fails.

---
## Module: `dw6/state_manager.py`

### `class Governor`
> Enforces the rules and permissions of the DW8 protocol.

The Governor acts as a security layer, ensuring that all actions performed
within the workflow adhere to the strict rules defined for each stage.
It maintains a rule set (`RULES`) that maps each stage to a list of
permitted commands or actions.

Attributes:
    state (WorkflowState): An instance of the workflow state manager.
    current_stage (str): The name of the current workflow stage.

#### `def governor_authorize(self, command: str)` (Dynamically Loaded)
> Authorizes or denies a command based on the current workflow stage.

This function acts as the central gatekeeper for command execution, enforcing
the principle that only certain commands are permissible in specific stages.

It operates by:
1.  Identifying the current workflow stage (e.g., 'Engineer', 'Coder').
2.  Looking up the list of allowed command prefixes for that stage in the
    `RULES` class attribute.
3.  Checking if the given `command` string starts with any of the authorized
    prefixes.

If the command is not authorized, it prints a denial message to standard
error and returns False, preventing the command from being executed.

Args:
    self (Governor): The instance of the Governor.
    command (str): The command string to be authorized.

Returns:
    bool: True if the command is authorized, False otherwise.

Side Effects:
    - Prints an error message to `sys.stderr` if authorization fails.

### `class WorkflowManager`
> The high-level orchestrator for the DW8 workflow.

The WorkflowManager acts as the central command processor. It receives
commands from the command-line interface (CLI), interprets them, and
delegates tasks to the appropriate components. It is the primary entry
point for user-driven actions like `approve`, `new`, and `status`.

It coordinates the actions of three key sub-components:
- Governor: Enforces the rules and permissions for the current workflow stage.
- WorkflowKernel: Executes the core logic of the workflow.
- WorkflowState: Manages the persistent state of the system.

Like other core components, it uses a dynamic method loading pattern,
sourcing its methods from files prefixed with `manager_` in the
`src/dw6/st/` directory.

Attributes:
    state (WorkflowState): An instance of the workflow state manager.
    governor (Governor): An instance of the rule-enforcing Governor.
    kernel (WorkflowKernel): An instance of the workflow kernel.
    current_stage_name (str): The name of the current workflow stage.
    current_event (dict | None): The event being processed.
    stage_module (module): The dynamically loaded module for the current stage.

#### `def manager__generate_context_restoration_report(self)` (Dynamically Loaded)
> Generates and displays a context restoration report for user verification.

This internal function is the final step in the AI Recovery Protocol. Its
purpose is to present the outcome of the context refresh procedure to the
user or operator for verification.

It operates by:
1.  Retrieving the concatenated context from the `__temp_restored_context`
    state variable, which was populated by the preceding refresh step.
2.  Printing this context to the console, clearly delineated as a formal report.
3.  Deleting the `__temp_restored_context` variable from the state to ensure
    no temporary data pollutes the workflow state going forward.

Args:
    self (WorkflowManager): The instance of the workflow manager.

Side Effects:
    - Prints a multi-line report to the console.
    - Deletes the `__temp_restored_context` key from the workflow state.

#### `def manager__load_stage_module(self)` (Dynamically Loaded)
> Dynamically loads and instantiates the module for the current stage.

This internal helper function is a cornerstone of the workflow's modular
design. It acts as a factory, responsible for providing the correct
stage-specific logic based on the current state of the workflow.

It uses a dictionary to map stage names (e.g., 'Engineer') to their
corresponding stage classes (e.g., `EngineerStage`). It then instantiates
the appropriate class, passing a reference to the workflow state object
to its constructor. This gives the stage module the context it needs to
perform its validation and other duties.

Args:
    self (WorkflowManager): The instance of the workflow manager.

Raises:
    ValueError: If `self.current_stage_name` does not correspond to a known
        stage class in the mapping dictionary.

Returns:
    object: An instantiated object of the current stage's class (e.g., an
        instance of `EngineerStage`).

#### `def manager__perform_context_refresh_procedure(self)` (Dynamically Loaded)
> Performs a full context refresh by reading critical project documents.

This internal function is a core component of the AI Recovery Protocol,
triggered when a `CognitiveCheckpoint` failure suggests context instability.
Its purpose is to rebuild a foundational understanding of the project by
reading a predefined list of canonical documents.

It iterates through a list of critical documents, such as:
- `docs/PROJECT_REQUIREMENTS.md`
- `docs/AI_PROTOCOL_TUTORIAL.md`
- `docs/protocols/DW8_PROTOCOL_DEFINITION.md`
- `README.md`

The contents of these files are concatenated and stored in a temporary
state variable, `__temp_restored_context`. This allows the restored context
to be passed to the next step in the recovery process, which is the
generation of a diagnostic report.

Args:
    self (WorkflowManager): The instance of the workflow manager.

Side Effects:
    - Reads multiple files from the `docs/` directory.
    - Sets the `__temp_restored_context` variable in the workflow state.
    - Prints status messages to the console.

#### `def manager_advance_requirement_pointer(self)` (Dynamically Loaded)
> Advances the RequirementPointer to the next requirement in the queue.

This function manages the sequential processing of requirements by manipulating
the `RequirementPointer` in the workflow state. It operates by:

1.  Scanning the `events/` directory for all `REQ-*.json` files.
2.  Sorting these files alphanumerically to establish a deterministic queue.
3.  Identifying the current requirement's position in this queue.
4.  Updating the `RequirementPointer` to the ID of the next file in the sequence.

It includes robust logic to handle initialization and recovery:
-   If the pointer is not set, it initializes it to the first requirement.
-   If the pointer references a file that no longer exists, it resets the
    pointer to the first requirement in the queue to prevent stalls.
-   If the end of the queue is reached, it reports this and makes no change.

Args:
    self (WorkflowManager): The instance of the workflow manager.

Returns:
    bool: True if the pointer was successfully advanced or reset; False if
        the end of the queue was reached or no requirements were found.

Side Effects:
    - Reads the contents of the `events/` directory.
    - Modifies the `RequirementPointer` value in the workflow state.
    - Prints status and error messages to the console.

#### `def manager_approve(self, needs_research=False, allow_failures=False)` (Dynamically Loaded)
> Orchestrates the approval and transition of a workflow stage.

This function is the primary entry point for the `approve` command. It manages
the validation of the current stage and the transition to the next, acting as
a central gatekeeper for the workflow's progression.

The process involves several key steps:
1.  **Context Retrieval:** Gathers details about the current stage and the active
    requirement.
2.  **Validation:** Calls the `validate()` method of the current stage's module
    to ensure all prerequisites for completion have been met.
3.  **Stage Advancement:** Determines the next stage based on the current stage
    and the requirement's type (e.g., 'Sherlock' requirements trigger a
    'Researcher' stage after 'Engineer'). It then calls the kernel's
    `advance_stage` method to execute the transition.
4.  **Error Handling:** Catches exceptions during validation. If `allow_failures`
    is False, it invokes the kernel's `_handle_failure` method. Otherwise,
    it logs the error and proceeds.

Args:
    self (WorkflowManager): The instance of the workflow manager.
    needs_research (bool, optional): A flag to manually force the workflow
        into the 'Researcher' stage. Defaults to False.
    allow_failures (bool, optional): If True, allows the stage to advance
        even if an exception occurs. Defaults to False.

Raises:
    Exception: If validation fails and `allow_failures` is False.

Side Effects:
    - Calls the `validate()` method of the current stage module.
    - Calls the kernel's `advance_stage()` and `_handle_failure()` methods.
    - Prints status and error messages to the console.
    - Saves the workflow state.

#### `def manager_archive_completed_event(self, event)` (Dynamically Loaded)
> Archives a completed event by moving it from the pending to the processed list.

This function manages the lifecycle of an event after it has been successfully
completed. It performs a simple but critical bookkeeping operation:

1.  Retrieves the `PendingEvents` and `ProcessedEvents` lists from the state.
2.  Removes the specified event from the `PendingEvents` list by matching its ID.
3.  Appends the event to the `ProcessedEvents` list.
4.  Saves the updated state to `workflow_state.json`.

This ensures that completed work is recorded and removed from the active queue.

Args:
    self (WorkflowManager): The instance of the workflow manager.
    event (dict): The event object that has been completed.

Side Effects:
    - Modifies the `PendingEvents` and `ProcessedEvents` lists in the workflow state.
    - Saves the updated state to the JSON file.

#### `def manager_check_context(self)` (Dynamically Loaded)
> Performs a context integrity check to detect potential state corruption.

This function implements a 'Cognitive Checkpoint', a simple yet effective
mechanism to verify the integrity of the workflow's state. It acts as a
canary in the coal mine.

The check involves retrieving a hardcoded value, 'Riko', from the
`CognitiveCheckpoint` key in the state file. If the value is missing or
does not match, it is considered a critical failure, indicating that the
context may be unstable or corrupt.

Upon failure, it triggers two recovery actions:
1.  `_perform_context_refresh_procedure()`: To reload and display the current state.
2.  `_generate_context_restoration_report()`: To create a diagnostic report.

Args:
    self (WorkflowManager): The instance of the workflow manager.

Side Effects:
    - Prints status and error messages to the console.
    - May trigger a full context refresh and report generation if the check fails.

#### `def manager_create_new_requirement(self, requirement_id, title, description, acceptance_criteria, event_type='Standard', priority='Normal')` (Dynamically Loaded)
> Creates a new requirement by delegating to the workflow kernel.

This function serves as the high-level entry point for creating new
requirement events. It acts as a wrapper, passing all provided arguments
directly to the corresponding method in the workflow kernel, which handles
the actual logic of creating the event file.

This separation of concerns keeps the manager interface clean while
concentrating the core business logic within the kernel.

Args:
    self (WorkflowManager): The instance of the workflow manager.
    requirement_id (str): The unique identifier for the new requirement (e.g., 'REQ-DW8-021').
    title (str): A brief, descriptive title for the requirement.
    description (str): A detailed explanation of the requirement's purpose.
    acceptance_criteria (list): A list of strings defining the conditions for completion.
    event_type (str, optional): The type of event (e.g., 'Standard', 'Deployment').
        Defaults to "Standard".
    priority (str, optional): The priority of the event (e.g., 'Normal', 'High').
        Defaults to "Normal".

Side Effects:
    - Calls the `create_new_requirement` method on the kernel instance, which
      in turn creates a new JSON file in the `events/` directory.

#### `def manager_get_current_event_details(self)` (Dynamically Loaded)
> Loads and returns the full details of the current requirement.

This function is responsible for fetching the complete context of the active
requirement. It retrieves the current requirement ID from the `RequirementPointer`
stored in the workflow state.

It then constructs the path to the corresponding JSON file located in the
`events/` directory and attempts to load and parse it. This function includes
robust error handling to manage several failure scenarios:

- If the `RequirementPointer` is not set.
- If the corresponding event file does not exist.
- If the event file is empty, corrupted, or cannot be read.

In any of these failure cases, a critical error message is printed to
standard error, and the function returns `None`.

Args:
    self (WorkflowManager): The instance of the workflow manager.

Returns:
    dict or None: A dictionary containing the detailed information of the
        current requirement on success, or `None` if any error occurs.

Side Effects:
    - Prints critical error messages to `sys.stderr` upon failure.

#### `def manager_show_status(self)` (Dynamically Loaded)
> Displays a comprehensive status report of the current workflow.

This function serves as the public entry point for the `status` command.
It acts as a simple wrapper, delegating the responsibility of generating
and displaying the detailed status report to the kernel's internal
`_perform_context_refresh` method.

This design separates the command interface (manager) from the core logic
(kernel), adhering to the system's architectural principles.

Args:
    self (WorkflowManager): The instance of the workflow manager.

Side Effects:
    - Triggers the printing of a detailed status report to the console via
      the kernel.

### `class WorkflowState`
> Manages the persistent state of the workflow via `workflow_state.json`.

This class is the single source of truth for the live operational state of
the DW8 system. It is responsible for reading, writing, and providing
access to critical state variables such as `CurrentStage`,
`RequirementPointer`, and various counters and statistics.

The class uses a dynamic method loading pattern. All state manipulation
methods (e.g., `get`, `set`, `save`, `load`) are defined in individual
files within the `src/dw6/st/` directory and are loaded at runtime.
This makes the state management system highly modular and extensible.

Attributes:
    state_file (Path): The path to the JSON file that stores the workflow state.
    data (dict): A dictionary holding the in-memory representation of the state.

#### `def add_pending_event(self, event, priority='Low')` (Dynamically Loaded)
> Adds a new event to the pending events queue based on its priority.

This function is responsible for adding new requirement events to the
`PendingEvents` list in the workflow state. It implements a priority-based
queueing system to allow for dynamic task management.

The insertion point of the new event is determined by its `priority`:
-   `High` or `Critical`: The event is inserted at the beginning of the queue,
    making it the next item to be processed.
-   `Medium`: The event is inserted into the middle of the queue.
-   `Low` (Default): The event is appended to the end of the queue.

This allows the workflow to respond to urgent tasks without losing track of
lower-priority items.

Args:
    self (WorkflowState): The instance of the workflow state manager.
    event (dict): The event object to be added to the queue.
    priority (str, optional): The priority of the event. Can be 'High',
        'Critical', 'Medium', or 'Low'. Defaults to "Low".

Side Effects:
    - Modifies the `PendingEvents` list in the workflow state.
    - Saves the updated state to the JSON file.

#### `def advance_requirement_pointer(self)` (Dynamically Loaded)
> Advances the RequirementPointer to the next event in the PendingEvents queue.
If the queue is empty, the pointer is set to None.

#### `def archive_completed_event(self, event_to_archive)` (Dynamically Loaded)
> Moves a completed event to the ProcessedEvents list.
This method assumes the event is the currently active one, not one from the pending queue.

#### `def create_red_flag_event(self, exception, stage)` (Dynamically Loaded)
> Creates a 'Red Flag' requirement in response to a critical failure.

This function is the system's ultimate safety net, designed to be called when
an unhandled exception occurs within the main workflow loop. It ensures that
critical failures are not lost and are instead converted into high-priority,
trackable work items.

The process involves:
1.  Dynamically generating a new requirement ID with the prefix `REQ-DW8-OS-`.
2.  Capturing the full details of the exception, including its type, message,
    and traceback.
3.  Creating a new event dictionary containing these details and a set of
    pre-defined acceptance criteria for debugging and resolution.
4.  Assigning the event a 'Critical' priority.
5.  Writing the event to a new JSON file in the `events/` directory.
6.  Adding the event to the front of the pending events queue using the
    `add_pending_event` method.

It also includes its own error handling in case the event creation process
itself fails.

Args:
    self (WorkflowManager): The instance of the workflow manager.
    exception (Exception): The unhandled exception object.
    stage (str): The name of the stage where the failure occurred.

Returns:
    str or None: The ID of the newly created Red Flag event, or None if the
        event creation process itself fails.

#### `def delete(self, key)` (Dynamically Loaded)
> Safely deletes a key-value pair from the workflow state.

This function provides a controlled interface for removing data from the
in-memory workflow state. It first checks for the existence of the key
before attempting to delete it, which prevents `KeyError` exceptions.

Note: This method only modifies the state in memory. The `save()` method
must be called separately to persist the changes to the `workflow_state.json`
file.

Args:
    self (WorkflowState): The instance of the workflow state manager.
    key (str): The key of the value to delete.

Side Effects:
    - Modifies the in-memory `self.data` dictionary if the key exists.

#### `def get(self, key, default=None)` (Dynamically Loaded)
> Safely retrieves a value from the workflow state by its key.

This function provides a controlled, read-only interface to the underlying
state data dictionary. It wraps the standard dictionary `get` method,
allowing other parts of the system to query the state without risking
a `KeyError` if a key does not exist.

Args:
    self (WorkflowState): The instance of the workflow state manager.
    key (str): The key of the value to retrieve.
    default (any, optional): The value to return if the key is not found.
        Defaults to None.

Returns:
    any: The value associated with the key, or the default value if the
        key is not present in the state data.

#### `def get_failure_counter(self, stage, counter_name='default')` (Dynamically Loaded)
> No docstring available.

#### `def increment(self, key)` (Dynamically Loaded)
> No docstring available.

#### `def increment_failure_counter(self, stage, counter_name='default')` (Dynamically Loaded)
> No docstring available.

#### `def initialize_state(self)` (Dynamically Loaded)
> No docstring available.

#### `def load(self)` (Dynamically Loaded)
> No docstring available.

#### `def reset_failure_counter(self, stage, counter_name='default')` (Dynamically Loaded)
> No docstring available.

#### `def save(self)` (Dynamically Loaded)
> Persists the in-memory workflow state to the JSON file on disk.

This method is the crucial final step in the state management lifecycle.
It takes the current in-memory `self.data` dictionary and writes it to the
`workflow_state.json` file.

It performs two key actions:
1.  Ensures that the parent directory for the state file exists, creating it
    if necessary.
2.  Serializes the `self.data` dictionary into a JSON string and writes it
    to the file. The output is formatted with an indent of 2 and sorted
    keys to ensure readability and consistent version control diffs.

Args:
    self (WorkflowState): The instance of the workflow state manager.

Side Effects:
    - Creates a directory if it doesn't exist.
    - Writes to the `workflow_state.json` file, overwriting its previous
      contents.

#### `def set(self, key, value)` (Dynamically Loaded)
> Sets or updates a value in the workflow state by its key.

This function provides the primary interface for modifying the in-memory
workflow state. It directly sets the `value` for the given `key` in the
underlying data dictionary.

Note: This method only modifies the state in memory. The `save()` method
must be called separately to persist the changes to the `workflow_state.json`
file.

Args:
    self (WorkflowState): The instance of the workflow state manager.
    key (str): The key of the value to set.
    value (any): The value to be stored.

Side Effects:
    - Modifies the in-memory `self.data` dictionary.

---
## Module: `dw6/templates.py`

### `def process_prompt(prompt_text: str, cycle_number: str)`
> Augments a raw user prompt and generates a formal technical specification markdown file.

---
## Module: `dw6/workflow/coder.py`

### `class CoderStage`
> Manages the 'Coder' stage of the DW8 workflow.

The Coder stage is the implementation phase where the technical plan
formulated during the 'Researcher' stage is turned into functional code.
The primary responsibility of this stage is to produce and commit code that
satisfies the requirements of the current task.

Attributes:
    state (WorkflowState): An instance of the workflow state manager.

#### `def validate(self, allow_failures=False)`
> Ensures new code has been committed before leaving the Coder stage.

This validation is a critical control point in the workflow. It checks
the Git repository to confirm that at least one new commit has been made
since the 'Coder' stage began. This is determined by comparing the current
HEAD commit SHA with the `CoderStartCommitSHA` stored in the workflow
state when the stage was entered.

This enforces the rule that all work must be captured in version control
before it can be passed to the 'Validator' stage.

Args:
    allow_failures (bool, optional): If True, allows the validation to
        pass even if no new commits are found. This is intended for
        exceptional circumstances. Defaults to False.

Returns:
    bool: True if a new commit is detected or if failures are allowed,
          False otherwise.

---
## Module: `dw6/workflow/deployer.py`

### `def _attach_methods()`
> No docstring available.

### `class DeployerStage`
> Manages the 'Deployer' stage of the DW8 workflow.

The Deployer stage is the final phase, responsible for versioning,
packaging, and releasing the software. It handles tasks such as creating
Git tags, pushing changes to the remote repository, and potentially
triggering a continuous integration/continuous deployment (CI/CD) pipeline.

Its operational methods, such as `validate`, are dynamically loaded from
the `dw6/workflow/dp/` subdirectory. This modular approach allows for
flexible and extensible deployment strategies.

Attributes:
    state (WorkflowState): An instance of the workflow state manager.

#### `def validate(self, allow_failures=False)`
> No docstring available.

#### `def chk_proj_cpl(self)` (Dynamically Loaded)
> Checks if all requirements in the master list are marked as Deployed.

#### `def exec_proto_evo(self)` (Dynamically Loaded)
> No docstring available.

#### `def exec_std_dep(self)` (Dynamically Loaded)
> No docstring available.

#### `def gen_final_readme(self)` (Dynamically Loaded)
> Generates the final README.md file for the project.

#### `def init(self, state)` (Dynamically Loaded)
> No docstring available.

#### `def ld_cfg(self)` (Dynamically Loaded)
> No docstring available.

#### `def validate(self, allow_failures=False)` (Dynamically Loaded)
> No docstring available.

---
## Module: `dw6/workflow/engineer.py`

### `class EngineerStage`
> Manages the 'Engineer' stage of the DW8 workflow.

The Engineer stage is the initial planning phase. Its primary responsibility
is to ensure that a high-level requirement has been broken down into a
clear, actionable, and sufficiently granular set of Sub-task Measurable
Requirements (SMRs). The deliverable for this stage is the updated
`docs/PROJECT_REQUIREMENTS.md` file.

Attributes:
    state (WorkflowState): An instance of the workflow state manager.

#### `def execute(self)`
> Confirms the planning phase is complete.

This method is a deliberate no-op. The "execution" of the Engineer
stage is the human- or AI-driven process of defining the SMRs. This
method simply serves as a formal step in the state machine before
validation occurs.

Returns:
    True, indicating the step is complete.

#### `def validate(self, allow_failures=False)`
> Ensures the current requirement has a sufficiently granular plan.

This method reads the `docs/PROJECT_REQUIREMENTS.md` file and verifies
that the requirement currently pointed to by the `RequirementPointer`
in the workflow state has at least two Sub-task Measurable Requirements
(SMRs). This enforces the principle of atomicity and prevents work from
starting on vague or monolithic tasks.

Args:
    allow_failures (bool, optional): A flag that is not currently used
        but is reserved for future flexibility. Defaults to False.

Returns:
    bool: True if the requirement has two or more SMRs, False otherwise.

Raises:
    Exception: Propagates any file I/O errors encountered during the
        reading of the requirements file.

---
## Module: `dw6/workflow/kernel.py`

### `class WorkflowKernel`
> The core engine of the DW8 workflow, orchestrating the state machine.

The WorkflowKernel is the heart of the system, responsible for executing the
fundamental logic of the development workflow. It is designed as a lean,
dynamically-loaded interface that orchestrates state transitions, processes
events, handles failures, and manages the overall lifecycle of a development
task according to the DW8 protocol.

Its modular design is a key feature. Most of its operational methods (e.g.,
`advance_stage`, `load_current_event_details`, `_handle_failure`) are
defined in individual files within the `src/dw6/workflow/kr/` subdirectory
and are loaded at runtime. This isolates logic, enhances maintainability,
and aligns with the Prism Protocol's goal of context stability.

Attributes:
    state (WorkflowState): An instance of the workflow state manager, providing
        access to the persistent state of the workflow.
    current_event (dict | None): The event dictionary currently being processed.
        Initialized to None.
    current_stage (str): The name of the current workflow stage, loaded from
        the state manager.
    python_executable_path (str): The absolute path to the Python executable
        in the active virtual environment.

#### `def _display_startup_summary(self)` (Dynamically Loaded)
> Displays a personalized startup summary at the beginning of a session.

This function provides immediate context to the user upon initialization of the
workflow. It constructs and prints a welcome message that includes:
- A personalized greeting using the user's name.
- The elapsed time since the user's last session.
- The ID of the currently active requirement.
- The name of the current workflow stage.

This information helps orient the user and confirms the system's state.

Args:
    self (WorkflowKernel): The instance of the workflow kernel, which provides
        access to `self.user_profile` and `self.state`.

Side Effects:
    Prints a formatted, multi-line summary to standard output.
    Prints an error to standard error if the user profile is not loaded.

#### `def _enter_rehearsal_stage(self, exception)` (Dynamically Loaded)
> Transitions the workflow into the 'Rehearsal' stage.

This function acts as a circuit breaker for the workflow. It is triggered
when a stage fails repeatedly, indicating a persistent problem that requires
deeper analysis. It performs the following critical actions:

1.  Creates a 'red flag' event, capturing the details of the exception
    that triggered the transition.
2.  Saves the current stage to `PreviousStage` for context.
3.  Sets the `CurrentStage` to 'Rehearsal'.
4.  Saves the updated state to `workflow_state.json`.

This forces a pause in the normal workflow, allowing for a focused
investigation and resolution of the root cause of the failure.

Args:
    self (WorkflowKernel): The instance of the workflow kernel.
    exception (Exception): The exception object that caused the failure.

Side Effects:
    - Prints a status message to standard error.
    - Modifies the workflow state by changing the current stage and
      recording the previous stage.
    - Creates a new red flag event file in the `events/` directory.
    - Saves the modified state to the filesystem.

#### `def _get_failure_context(self)` (Dynamically Loaded)
> Constructs a failure tracking key and retrieves the current count.

This helper function is central to the workflow's resilience mechanism.
It generates a unique key for tracking failures based on a combination of
the current requirement ID and the current workflow stage. It then uses
this key to look up the number of consecutive failures that have occurred
under these exact circumstances.

This allows the system to implement policies based on repeated failures,
such as triggering the 'Rehearsal' stage.

Args:
    self (WorkflowKernel): The instance of the workflow kernel, providing
        access to `self.current_event`, `self.current_stage`, and `self.state`.

Returns:
    tuple[str, int]: A tuple containing:
        - The constructed failure key (e.g., 'failure_count_REQ-001_Coder').
        - The current number of consecutive failures for that key.

#### `def _handle_failure(self, exception)` (Dynamically Loaded)
> Manages the workflow's response to a failure within a stage.

This function is the core of the system's resilience mechanism. When a
recoverable error occurs, this function is called to orchestrate the
response. It increments the failure counter for the current stage and
requirement.

If the number of consecutive failures meets or exceeds the `FAILURE_THRESHOLD`,
it triggers a transition to the 'Rehearsal' stage by calling
`_enter_rehearsal_stage`. This acts as a circuit breaker, preventing the
system from getting stuck in a loop of repeated failures.

If the threshold has not been reached, it simply logs the failure and allows
the system to proceed, typically for a retry attempt.

Args:
    self (WorkflowKernel): The instance of the workflow kernel.
    exception (Exception): The exception object that represents the failure.

Side Effects:
    - Prints status messages to standard error.
    - Increments a failure counter in the workflow state.
    - May trigger a stage transition by calling `_enter_rehearsal_stage`.

#### `def _load_environment(self)` (Dynamically Loaded)
> Loads and validates the environment variables from the .env file.

This function is a critical part of the workflow's initialization sequence.
It ensures that the operating environment is correctly configured before any
substantive work begins. It performs two main checks:

1.  It locates and loads the `.env` file from the project's root directory.
2.  It verifies that the `GITHUB_TOKEN` variable is present in the loaded
    environment.

If either of these checks fails, it raises a critical exception, halting
the workflow to prevent execution with an incomplete or invalid
configuration.

Args:
    self (WorkflowKernel): The instance of the workflow kernel.

Raises:
    FileNotFoundError: If the `.env` file cannot be found in the project tree.
    ValueError: If the `GITHUB_TOKEN` environment variable is not set.

Side Effects:
    - Loads environment variables from the `.env` file into the process's
      environment using `dotenv`.
    - Prints status messages to standard output.

#### `def _manage_user_profile(self)` (Dynamically Loaded)
> Manages the user profile for session continuity and personalization.

This function is responsible for loading, creating, and updating the user's
profile, which is stored in `data/user_profile.json`. The profile contains
the user's name and the timestamp of their last session.

On initialization, it performs the following actions:
1.  Checks if running under `pytest` and, if so, loads a mock profile to
    ensure test isolation and predictability.
2.  If not testing, it reads the profile from the JSON file.
3.  If the profile is new or does not contain a user name, it prompts the
    user for their name. It includes error handling for non-interactive
    environments, where it assigns a default name.
4.  It updates the `last_session_timestamp` to the current time.
5.  It saves the updated profile back to the JSON file.
6.  It attaches the loaded profile to the kernel instance (`self.user_profile`)
    for easy access throughout the session.

Args:
    self (WorkflowKernel): The instance of the workflow kernel.

Side Effects:
    - Reads from and writes to `data/user_profile.json`.
    - May prompt the user for input via the console.
    - Prints status messages to standard output and standard error.
    - Sets the `self.user_profile` attribute on the kernel instance.

#### `def _perform_context_refresh(self)` (Dynamically Loaded)
> Displays a comprehensive status report for the current workflow state.

This function serves as the primary information source for the `dw6 status`
command. It provides a detailed snapshot of the current operational context,
which includes:

- The current cycle counter.
- The name of the active workflow stage.
- A detailed breakdown of the current requirement (event), including its
  title, description, and the status of its acceptance criteria (SMRs).
- The contents of the `AI_PROTOCOL_TUTORIAL.md` to provide the operator
  with essential guidance on interacting with the system.

This function is crucial for maintaining situational awareness and ensuring
that the user or AI has all the necessary information to proceed with the
current task.

Args:
    self (WorkflowKernel): The instance of the workflow kernel, providing
        access to `self.state` and `self.current_event`.

Side Effects:
    - Prints a detailed, multi-section status report to standard output.
    - Reads from the `docs/AI_PROTOCOL_TUTORIAL.md` file if it exists.

#### `def _reset_failure_counters(self, stage)` (Dynamically Loaded)
> Resets the failure counter for a specific stage and requirement.

This function is a key component of the workflow's resilience strategy.
It is called when a stage completes successfully to reset the associated
failure counter to zero. This ensures that the system does not retain a
memory of past, resolved failures, allowing for a clean slate when the
same stage is encountered again in a different context.

The function constructs a unique failure key based on the current requirement
ID and the specified stage, then sets its value to 0 in the workflow state.

Args:
    self (WorkflowKernel): The instance of the workflow kernel.
    stage (str): The name of the stage for which to reset the counter.

Side Effects:
    - Modifies the workflow state by setting a specific failure counter to 0.
    - The change is not immediately saved to disk; a subsequent `self.state.save()`
      is required.

#### `def advance_stage(self, needs_research=False)` (Dynamically Loaded)
> Advances the workflow to the next stage, implementing the core state machine.

This function is the heart of the DW8 protocol's state machine. It determines
the next logical stage based on the current stage and the context of the
workflow (e.g., whether it's a standard requirement or a protocol update).

The function orchestrates two primary workflow paths:
1.  **Standard Workflow:** The typical progression from `Engineer` -> `Researcher`
    -> `Coder` -> `Validator` -> `Deployer` and back to `Engineer` upon
    completion. It also handles the transition out of the `Rehearsal` stage.
2.  **Protocol Update Interrupt:** A specialized, shortened workflow for
    updating the protocol itself (`Engineer` -> `Coder` -> `Validator`).

Beyond just changing the stage, this function performs several critical
side effects to manage the workflow's state and integrity:
- Records detailed timing statistics for each stage.
- Resets failure counters upon successful stage completion.
- Archives completed events and advances the requirement pointer.
- Records the starting commit SHA when entering the `Coder` stage to ensure
  new work is committed.

Args:
    self (WorkflowKernel): The instance of the workflow kernel.
    needs_research (bool, optional): A flag indicating if the 'Researcher'
        stage should be entered after 'Engineer'. Defaults to False.

Raises:
    Exception: If an unknown or invalid stage transition is attempted, which
        typically indicates state corruption.

Side Effects:
    - Modifies and saves the `workflow_state.json` file with the new stage
      and other updated metadata.
    - Prints numerous status messages to standard output.
    - Updates the kernel's internal `self.current_stage` attribute.
    - Interacts with the Git repository to get the latest commit hash.

#### `def create_new_requirement(self, requirement_id, title, description, acceptance_criteria, event_type='Standard', priority='Normal')` (Dynamically Loaded)
> Creates a new requirement JSON file and adds a corresponding event to the pending queue.

---
## Module: `dw6/workflow/rehearsal.py`

### `class RehearsalStage`
> No docstring available.

#### `def validate(self, allow_failures=False)`
> This stage forces the AI to reflect on repeated failures, analyze the
root cause, and propose alternative solutions before retrying.

---
## Module: `dw6/workflow/researcher.py`

### `class ResearcherStage`
> Manages the 'Researcher' stage of the DW8 workflow.

The Researcher stage is dedicated to investigation and information gathering.
During this phase, the AI uses various tools to explore the codebase,
search for external documentation, and analyze existing implementations
to formulate a robust technical plan. The primary deliverable is a
well-defined solution design that will guide the subsequent 'Coder' stage.

Attributes:
    state (WorkflowState): An instance of the workflow state manager.

#### `def validate(self, allow_failures=False)`
> Validates the output of the research phase.

This method is currently a placeholder. In a future implementation, it
will be responsible for verifying that the research activities have
produced a concrete design document or implementation plan before the
workflow is allowed to proceed to the 'Coder' stage.

Args:
    allow_failures (bool, optional): A flag reserved for future use.
        Defaults to False.

Returns:
    True, as no validation is currently implemented.

---
## Module: `dw6/workflow/validator.py`

### `class ValidatorStage`
> Manages the 'Validator' stage of the DW8 workflow.

The Validator stage acts as the quality assurance gate. Its primary function
is to run the project's automated test suite to verify the correctness and
stability of the code produced in the 'Coder' stage. It ensures that new
changes have not introduced regressions and that the software meets all
specified requirements.

It explicitly uses `uv run pytest` to guarantee that tests are executed
within the project's designated virtual environment, preventing environment-related
discrepancies.

Attributes:
    state (WorkflowState): An instance of the workflow state manager.

#### `def validate(self, allow_failures=False)`
> Executes the project's test suite using `pytest`.

This method runs the test suite via a subprocess call to `uv run pytest`.
On success, it resets the 'Validator' failure counter. On failure, it
increments the counter and prints the error output.

This validation step is crucial for maintaining code quality and ensuring
that only verified code proceeds to the 'Deployer' stage.

Args:
    allow_failures (bool, optional): If True, allows the stage to be
        approved even if tests fail. This is intended for exceptional
        cases. Defaults to False.

Returns:
    bool: True if the tests pass or if failures are allowed, False
          otherwise.

---
