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
> The Governor enforces the rules of the DW8 protocol, ensuring that
only authorized actions are performed in each stage of the workflow.

### `class WorkflowManager`
> The WorkflowManager is the high-level orchestrator. It interprets user
commands and directs the WorkflowKernel and Stage modules to execute
the appropriate actions.

### `class WorkflowState`
> The WorkflowState class manages the persistent state of the workflow,
reading from and writing to the `workflow_state.json` file.

---
## Module: `dw6/templates.py`

### `def process_prompt(prompt_text: str, cycle_number: str)`
> Augments a raw user prompt and generates a formal technical specification markdown file.

---
## Module: `dw6/workflow/coder.py`

### `class CoderStage`
> No docstring available.

#### `def validate(self, allow_failures=False)`
> No docstring available.

---
## Module: `dw6/workflow/deployer.py`

### `def _attach_methods()`
> No docstring available.

### `class DeployerStage`
> Handles the deployment of the project by dynamically loading methods.

#### `def validate(self, allow_failures=False)`
> No docstring available.

---
## Module: `dw6/workflow/engineer.py`

### `class EngineerStage`
> No docstring available.

#### `def execute(self)`
> The Engineer stage's execution is a no-op. The plan is already defined.

#### `def validate(self, allow_failures=False)`
> Ensures the current requirement is broken down into atomic sub-tasks.

---
## Module: `dw6/workflow/kernel.py`

### `class WorkflowKernel`
> The DW8 Workflow Kernel.

This class serves as a lean interface that dynamically loads its methods
from individual files within the 'kr' subdirectory. This modular design,
mandated by Riko, enhances maintainability and reduces context instability
by isolating method implementations.

The kernel orchestrates the entire development workflow, managing state
transitions, event handling, and failure recovery based on the DW8 protocol.

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
> No docstring available.

#### `def validate(self, allow_failures=False)`
> No docstring available.

---
## Module: `dw6/workflow/validator.py`

### `class ValidatorStage`
> No docstring available.

#### `def validate(self, allow_failures=False)`
> Runs tests using `uv run pytest` to ensure execution within the
correct virtual environment.

---
## Module: `dw6/workflow/dp/chk_proj_cpl.py`

### `def _check_if_project_is_complete(self)`
> Checks if all requirements in the master list are marked as Deployed.

---
## Module: `dw6/workflow/dp/exec_proto_evo.py`

### `def _execute_protocol_evolution(self)`
> No docstring available.

---
## Module: `dw6/workflow/dp/exec_std_dep.py`

### `def _execute_standard_deployment(self)`
> No docstring available.

---
## Module: `dw6/workflow/dp/gen_final_readme.py`

### `def _generate_final_readme(self)`
> Generates the final README.md file for the project.

---
## Module: `dw6/workflow/dp/init.py`

### `def __init__(self, state)`
> No docstring available.

---
## Module: `dw6/workflow/dp/ld_cfg.py`

### `def _load_config(self)`
> No docstring available.

---
## Module: `dw6/workflow/dp/validate.py`

### `def validate(self, allow_failures=False)`
> No docstring available.

---
## Module: `dw6/workflow/kr/_advance_requirement_pointer.py`

### `def _advance_requirement_pointer(self)`
> No docstring available.

---
## Module: `dw6/workflow/kr/_complete_event_in_queue.py`

### `def _complete_event_in_queue(self)`
> Moves the current event from the pending queue to the processed queue.

---
## Module: `dw6/workflow/kr/_create_red_flag_requirement.py`

### `def _create_red_flag_requirement(self, exception)`
> Creates a special 'Red Flag' requirement when a critical failure threshold is met.
This requirement is prioritized to force a manual, intelligent review of the failure.

---
## Module: `dw6/workflow/kr/_display_startup_summary.py`

### `def _display_startup_summary(self)`
> Displays a personalized startup message including the user's name,
time since last session, and a summary of the current project status.

---
## Module: `dw6/workflow/kr/_enter_rehearsal_stage.py`

### `def _enter_rehearsal_stage(self, exception)`
> No docstring available.

---
## Module: `dw6/workflow/kr/_get_failure_context.py`

### `def _get_failure_context(self)`
> No docstring available.

---
## Module: `dw6/workflow/kr/_handle_failure.py`

### `def _handle_failure(self, exception)`
> No docstring available.

---
## Module: `dw6/workflow/kr/_load_environment.py`

### `def _load_environment(self)`
> No docstring available.

---
## Module: `dw6/workflow/kr/_load_event_details.py`

### `def _load_event_details(self, event_summary)`
> Loads the full details of an event from its JSON file, constructing
the self.current_event object.

---
## Module: `dw6/workflow/kr/_manage_user_profile.py`

### `def _manage_user_profile(self)`
> Manages the user profile, creating it if it doesn't exist and
updating the last session timestamp.

---
## Module: `dw6/workflow/kr/_perform_context_refresh.py`

### `def _perform_context_refresh(self)`
> Displays a detailed status report of the current workflow state, including
the active requirement's details and the AI Protocol Tutorial.
This method serves as the primary output for the `dw6 status` command.

---
## Module: `dw6/workflow/kr/_reset_failure_counters.py`

### `def _reset_failure_counters(self, stage)`
> No docstring available.

---
## Module: `dw6/workflow/kr/advance_stage.py`

### `def advance_stage(self, needs_research=False)`
> Advances the workflow to the next stage based on the current stage and event type.
This method implements the core state machine logic of the DW8 protocol.

---
## Module: `dw6/workflow/kr/create_new_requirement.py`

### `def create_new_requirement(self, requirement_id, title, description, acceptance_criteria, event_type='Standard', priority='Normal')`
> Creates a new requirement JSON file and adds a corresponding event to the pending queue.

---
## Module: `dw6/workflow/kr/load_current_event_details.py`

### `def load_current_event_details(self)`
> Finds the current event summary from the pending queue based on the
RequirementPointer and triggers the loading of its full details.

---
## Module: `dw6/st/add_pending_event.py`

### `def add_pending_event(self, event, priority='Low')`
> Adds a new event to the pending events queue according to its priority.

---
## Module: `dw6/st/archive_completed_event.py`

### `def archive_completed_event(self, event)`
> Moves a completed event from the pending queue to the processed queue.

---
## Module: `dw6/st/delete.py`

### `def delete(self, key)`
> No docstring available.

---
## Module: `dw6/st/get.py`

### `def get(self, key, default=None)`
> No docstring available.

---
## Module: `dw6/st/get_failure_counter.py`

### `def get_failure_counter(self, stage, counter_name='default')`
> No docstring available.

---
## Module: `dw6/st/governor_authorize.py`

### `def authorize(self, command: str)`
> Checks if a command is allowed in the current stage.

---
## Module: `dw6/st/increment.py`

### `def increment(self, key)`
> No docstring available.

---
## Module: `dw6/st/increment_failure_counter.py`

### `def increment_failure_counter(self, stage, counter_name='default')`
> No docstring available.

---
## Module: `dw6/st/initialize_state.py`

### `def initialize_state(self)`
> No docstring available.

---
## Module: `dw6/st/load.py`

### `def load(self)`
> No docstring available.

---
## Module: `dw6/st/manager__generate_context_restoration_report.py`

### `def _generate_context_restoration_report(self)`
> Generates a summary of the restored context for user verification.

---
## Module: `dw6/st/manager__load_stage_module.py`

### `def _load_stage_module(self)`
> No docstring available.

---
## Module: `dw6/st/manager__perform_context_refresh_procedure.py`

### `def _perform_context_refresh_procedure(self)`
> Reads all critical project documents to rebuild context.

---
## Module: `dw6/st/manager_approve.py`

### `def approve(self, needs_research=False, allow_failures=False)`
> No docstring available.

---
## Module: `dw6/st/manager_check_context.py`

### `def check_context(self)`
> Performs a context integrity check.

---
## Module: `dw6/st/manager_create_new_requirement.py`

### `def create_new_requirement(self, requirement_id, title, description, acceptance_criteria, event_type='Standard', priority='Normal')`
> No docstring available.

---
## Module: `dw6/st/manager_show_status.py`

### `def show_status(self)`
> Displays the context of the current event and stage.

---
## Module: `dw6/st/reset_failure_counter.py`

### `def reset_failure_counter(self, stage, counter_name='default')`
> No docstring available.

---
## Module: `dw6/st/save.py`

### `def save(self)`
> No docstring available.

---
## Module: `dw6/st/set.py`

### `def set(self, key, value)`
> No docstring available.

---
