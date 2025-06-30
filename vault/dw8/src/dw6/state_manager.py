import re
import sys
import os
import subprocess
import shutil
import git
import traceback
from pathlib import Path
from datetime import datetime, timezone

MASTER_FILE = "docs/WORKFLOW_MASTER.md"
REQUIREMENTS_FILE = "docs/PROJECT_REQUIREMENTS.md"
APPROVAL_FILE = "logs/approvals.log"
FAILURE_THRESHOLD = 3
STAGES = ["Engineer", "Researcher", "Coder", "Validator", "Deployer"]
DELIVERABLE_PATHS = {
    "Engineer": "deliverables/engineering",
    "Researcher": "deliverables/research",
    "Coder": "deliverables/coding",
    "Validator": "deliverables/testing",
    "Deployer": "deliverables/deployment",
}

class Governor:
    RULES = {
        "Engineer": [
            "uv run python -m dw6.main new",
            "uv run python -m dw6.main meta-req",
            "ls",
            "cat",
            "view_file_outline",
            "uv run python -m dw6.main approve"
        ],
        "Researcher": [
            "searxng_web_search",
            "web_url_read",
            "mcp0_get-library-docs",
            "codebase_search",
            "view_file_outline",
            "view_line_range",
            "mcp3_read_file",
            "ls",
            "uv run python -m dw6.main approve"
        ],
        "Coder": [
            "replace_file_content",
            "write_to_file",
            "view_file_outline",
            "ls",
            "mkdir",
            "uv run python -m dw6.main approve"
        ],
        "Validator": [
            "uv run python -m pytest",
            "uv run python -m dw6.main approve"
        ],
        "Deployer": [
            "git add",
            "git commit",
            "git tag",
            "uv run python -m dw6.main approve"
        ]
    }

    def __init__(self, state):
        self.state = state
        self.current_stage = self.state.get("CurrentStage")

    def authorize(self, command: str):
        """Checks if a command is allowed in the current stage."""
        allowed_commands = self.RULES.get(self.current_stage, [])
        if not any(command.startswith(prefix) for prefix in allowed_commands):
            error_msg = f"[GOVERNOR] Action denied. The command '{command}' is not allowed in the '{self.current_stage}' stage."
            print(error_msg, file=sys.stderr)
            raise PermissionError(error_msg)
        print(f"[GOVERNOR] Action authorized: '{command}'")

class WorkflowManager:
    def __init__(self):
        self.state = WorkflowState()
        self.current_stage = self.state.get("CurrentStage", "Engineer")
        self.previous_stage = None
        self.governor = Governor(self.state)

    def approve(self, allow_failures=False, needs_research=False):
        print(f"--- Governor: Received Approval Request for Stage: {self.current_stage} ---")
        self.governor.authorize(f'uv run python -m dw6.main approve')
        
        try:
            if self._validate_stage_exit_criteria(allow_failures=allow_failures):
                print("Stage validation successful.")
                self._advance_stage(needs_research=needs_research)
            else:
                raise Exception("Stage validation failed without an exception.")
        except Exception as e:
            self._handle_failure(e)

    def _print_rules(self):
        rules = self.governor.RULES.get(self.current_stage, [])
        print("[RULE] Allowed command prefixes:")
        for prefix in rules:
            print(f"  - {prefix}")

    def _validate_stage_exit_criteria(self, allow_failures=False):
        """Checks if the current stage's exit criteria are met."""
        print(f"Governor: Validating exit criteria for stage: {self.current_stage}")
        if self.current_stage == "Validator":
            return self._validate_tests(allow_failures)
        elif self.current_stage == "Deployer":
            return self._validate_deployment()
        
        print(f"Governor: No specific exit criteria for '{self.current_stage}'. Approved by default.")
        return True

    def _complete_cycle(self):
        """Handles the completion of a full workflow cycle."""
        print("--- Governor: Final stage approved. Workflow complete. Cycling back to Engineer. ---")
        self._log_approval()
        self.state.increment("CycleCounter")

    def _advance_stage(self, needs_research=False):
        self.previous_stage = self.current_stage
        
        if self.previous_stage == "Deployer":
            self._complete_cycle()
            new_stage = "Engineer"
        else:
            current_index = STAGES.index(self.previous_stage)
            if self.previous_stage == "Engineer":
                new_stage = "Researcher" if needs_research else "Coder"
            elif current_index < len(STAGES) - 1:
                new_stage = STAGES[current_index + 1]
            else: # Should not be reached if Deployer is last
                self._complete_cycle()
                new_stage = "Engineer"

        self.current_stage = new_stage
        self.state.set("CurrentStage", self.current_stage)
        self._reset_failure_counters(self.previous_stage)
        self.state.save()
        self._run_post_transition_actions()
        print(f"--- Governor: Stage {self.previous_stage} Approved. New Stage: {self.current_stage} ---")

    def _log_approval(self):
        """Logs the approval of the current requirement."""
        requirement = self.state.get("Requirement")
        timestamp = datetime.now(timezone.utc).isoformat()
        with open(APPROVAL_FILE, "a") as f:
            f.write(f"{timestamp} - Requirement '{requirement}' approved.\n")

    def _run_post_transition_actions(self):
        if self.current_stage == "Engineer":
            self._ensure_atomic_requirement()
        elif self.previous_stage == "Coder":
            self.save_current_commit_sha()
            self._generate_coder_deliverable()

    def _ensure_atomic_requirement(self):
        """Ensures the current requirement is broken down into atomic sub-tasks."""
        print("--- Governor: Checking for atomic requirement... ---")
        try:
            req_pointer = self.state.get("RequirementPointer")
            if not req_pointer:
                print("RequirementPointer not found in state. Skipping check.")
                return

            req_id = f"REQ-DW8-{int(req_pointer):03d}"
            print(f"Current requirement ID: {req_id}")

            with open(REQUIREMENTS_FILE, "r") as f:
                content = f.read()

            # Regex to find the requirement block from its ID to the next separator
            # (?s) flag makes . match newlines
            match = re.search(rf"(?s)### ID: {re.escape(req_id)}\n(.*?)(?=\n---\n|\Z)", content)

            if match:
                requirement_text = match.group(1).strip()
                # Analyze the SMR checklist for granularity
                smr_section_match = re.search(r"- \*\*SMRs:\*\*\n((?:  - .+\n?)+)", requirement_text, re.MULTILINE)

                if smr_section_match:
                    smr_block = smr_section_match.group(1)
                    # Count non-empty lines starting with '  - [ ]'
                    smr_count = len(re.findall(r"^  - \[", smr_block, re.MULTILINE))
                    print(f"Found {smr_count} SMRs.")

                    if smr_count < 2:
                        print("\n[GOVERNOR] HALT: Requirement is not sufficiently granular.", file=sys.stderr)
                        print(f"The current requirement '{req_id}' has fewer than 2 sub-tasks.", file=sys.stderr)
                        print("Please break it down further using a future 'dw6 breakdown' command.", file=sys.stderr)
                        sys.exit(1)
                    else:
                        print("Requirement passes granularity check.")
                else:
                    print(f"\n[GOVERNOR] HALT: No SMRs found for requirement '{req_id}'.", file=sys.stderr)
                    print("Please define sub-requirements using a future 'dw6 breakdown' command.", file=sys.stderr)
                    sys.exit(1)
            else:
                print(f"Could not find requirement block for ID: {req_id}")

        except Exception as e:
            print(f"Error during atomic requirement check: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    def _generate_coder_deliverable(self):
        from dw6 import git_handler
        cycle = self.state.get("CycleCounter")
        req_pointer = self.state.get("RequirementPointer")
        commit_sha = self.state.get(f"CommitSHA.{self.previous_stage}")
        if not commit_sha:
            print(f"No commit SHA found for stage {self.previous_stage}. Skipping deliverable generation.")
            return

        changed_files, diff = git_handler.get_changes_since_last_commit(commit_sha)
        deliverable_path = Path(DELIVERABLE_PATHS["Coder"]) / f"cycle_{cycle}_coder_deliverable.md"
        deliverable_path.parent.mkdir(parents=True, exist_ok=True)
        with open(deliverable_path, "w") as f:
            f.write(f"# Coder Stage Deliverable for Requirement {req_pointer}\n\n")
            f.write("## Changed Files\n\n")
            f.write('\n'.join(f"- `{file}`" for file in changed_files))
            f.write("\n\n## Diff\n\n")
            f.write("```diff\n")
            f.write(diff)
            f.write("\n```")
        print(f"Generated Coder deliverable at {deliverable_path}")

    def _handle_failure(self, exception):
        failure_key = f"FailureCounters.{self.current_stage}.{self._get_failure_context()}"
        new_count = self.state.increment(failure_key)
        print(f"[FAILURE_COUNTER] Incremented '{failure_key}' to {new_count}.")

        if new_count >= FAILURE_THRESHOLD:
            print("--- Failure threshold reached. Activating Escalation Protocol. ---", file=sys.stderr)
            self._create_red_flag_requirement(exception)
            print("--- Resetting to Engineer stage. ---", file=sys.stderr)
            self.state.set("CurrentStage", "Engineer")
            self.state.save()
            sys.exit(1) # Terminate the current failed run
        else:
            print(f"--- Governor: Stage {self.current_stage} Approval Failed. Halting. ---")
            sys.exit(1)

    def _get_failure_context(self):
        if self.current_stage == "Validator":
            return self._validate_tests.__name__
        elif self.current_stage == "Deployer":
            return self._validate_deployment.__name__
        return "default"

    def _reset_failure_counters(self, stage):
        prefix = f"FailureCounters.{stage}."
        keys_to_reset = [k for k in self.state.data.keys() if k.startswith(prefix)]
        for key in keys_to_reset:
            self.state.set(key, 0)
            print(f"[FAILURE_COUNTER] Reset '{key}' to 0.")

    def save_current_commit_sha(self):
        from dw6 import git_handler
        commit_sha = git_handler.get_latest_commit_hash()
        self.state.set(f"CommitSHA.{self.current_stage}", commit_sha)
        self.state.save()
        print(f"Saved current commit SHA for {self.current_stage} stage: {commit_sha[:7]}")

    def _validate_tests(self, allow_failures=False):
        print("Validating tests...")
        python_executable = self.state.get("PythonExecutablePath")
        if not python_executable:
            raise FileNotFoundError("Python executable path not found in state.")
        try:
            subprocess.run([python_executable, "-m", "pytest"], check=True, capture_output=True, text=True)
            print("All tests passed.")
            return True
        except subprocess.CalledProcessError as e:
            print("--- Test Failures Detected ---", file=sys.stderr)
            print(e.stdout, file=sys.stderr)
            print(e.stderr, file=sys.stderr)
            if allow_failures:
                print("WARNING: Test failures detected, but approval is forced.", file=sys.stderr)
                return True
            raise e

    def _validate_deployment(self):
        from dw6 import git_handler
        print("Validating deployment readiness...")

        is_protocol_update = self.state.get("is_protocol_update") == 'true'

        if is_protocol_update:
            print("Protocol update detected. Executing evolution sub-workflow...")
            return self._execute_protocol_evolution()
        else:
            print("Standard deployment process...")
            try:
                commit_sha = git_handler.mcp_push_files("feat: Coder stage submission", ["src", "tests"])
                if not commit_sha:
                    print("Deployment validation failed: No commit SHA returned from push.", file=sys.stderr)
                    return False
                cycle = self.state.get("CycleCounter")
                tag_name = f"v1.{cycle}"
                git_handler.mcp_create_and_push_tag(tag_name, commit_sha, f"Release for cycle {cycle}")
                print("Deployment validation successful.")
                return True
            except Exception as e:
                print(f"Deployment validation failed: {e}", file=sys.stderr)
                raise e

    def _execute_protocol_evolution(self):
        from dw6 import git_handler
        print("Executing protocol evolution...")

        try:
            # 1. Determine new protocol version
            project_root = git_handler.get_project_root()
            current_project_name = project_root.name
            match = re.search(r'dw(\d+)', current_project_name)
            if not match:
                print(f"ERROR: Could not determine protocol version from project name '{current_project_name}'", file=sys.stderr)
                return False
            
            current_version = int(match.group(1))
            new_version = current_version + 1
            new_protocol_dir_name = f"dw{new_version}"
            # Create paths inside the current repo
            new_protocol_path = project_root / new_protocol_dir_name

            # 2. Create new protocol directory and copy files
            if new_protocol_path.exists():
                shutil.rmtree(new_protocol_path)
            # Copy the 'src' and 'docs' directories to the new protocol folder
            shutil.copytree(project_root / 'src', new_protocol_path / 'src')
            shutil.copytree(project_root / 'docs', new_protocol_path / 'docs')
            print(f"Successfully copied project source to {new_protocol_path}")

            # 3. Create new start script inside the new protocol directory
            new_start_script_name = f"start-project-{new_protocol_dir_name}.md"
            new_start_script_path = new_protocol_path / new_start_script_name
            script_template = f'---\ndescription: A guided workflow for initializing new projects using the {new_protocol_dir_name.upper()} protocol.\n---\n# {new_protocol_dir_name.upper()} Project Initialization\nThis workflow sets up a new project based on the {new_protocol_dir_name.upper()} protocol. NOTE: This start script is part of the release artifact. To use it, copy it to your `.windsurf/workflows/` directory.'
            with open(new_start_script_path, "w") as f:
                f.write(script_template)
            print(f"Successfully created new start script at {new_start_script_path}")

            # 4. Generate README.md
            new_readme_path = new_protocol_path / "README.md"
            readme_template = f'# DW{new_version} Protocol\n\n## Overview\nThe DW{new_version} protocol represents an evolution in the development workflow, focusing on robustness, self-reflection, and automated release management.\n\n## Workflow Diagram\n`Engineer` -> `Coder` -> `Validator` -> `Deployer`\n   ^            |\n   |         (failure)\n   +------- `Rehearsal`\n\n## Version Changelog (vs DW{current_version})\n- **Implemented `Rehearsal` State:** A mandatory \'time-out\' state triggered by consecutive failures.\n- **Formalized Protocol Evolution:** The `Deployer` stage now includes a sub-workflow to automatically version, document, and release new protocol updates.'
            with open(new_readme_path, "w") as f:
                f.write(readme_template)
            print(f"Successfully created README.md at {new_readme_path}")

            # 5. Commit and push new protocol to the current repo
            master_repo = git.Repo(project_root)
            # Add the newly created protocol directory
            files_to_add = [str(new_protocol_path)]
            master_repo.git.add(files_to_add)
            commit_message = f"feat(DW): Release new protocol DW{new_version}"
            master_repo.git.commit('-m', commit_message)
            print(f"Committed changes with message: '{commit_message}'")
            git_handler.push_to_remote(repo=master_repo)

            print("Protocol evolution successful.")
            return True

        except Exception as e:
            print(f"ERROR: Failed during protocol evolution: {e}", file=sys.stderr)
            raise e

    def _create_red_flag_requirement(self, exception):
        print("--- Creating Red Flag requirement... ---", file=sys.stderr)
        try:
            with open(REQUIREMENTS_FILE, "r+") as f:
                content = f.read()
                req_ids = [int(num) for num in re.findall(r"REQ-DW8-(\d+)", content)]
                next_id = max(req_ids) + 1 if req_ids else 1
                new_req_id = f"REQ-DW8-{next_id:03d}"

                exc_type = type(exception).__name__
                exc_message = str(exception).replace('\n', '\n    ')
                tb_str = "".join(traceback.format_tb(exception.__traceback__)).replace('\n', '\n      ')

                red_flag_template = f"""
---

### ID: {new_req_id}

- **Title:** Red Flag: Unhandled Critical Failure in {self.current_stage} Stage
- **Status:** `Pending`
- **Priority:** `Critical`
- **Details:** The workflow encountered a critical failure after multiple retries. The system has been reset to the Engineer stage to re-evaluate the approach.
- **SMRs:**
  - [ ] Analyze the failure context below to understand the root cause.
  - [ ] Formulate a new plan to address the failure.
  - [ ] Implement the new plan.
- **Failure Context:**
  - **Exception Type:** `{exc_type}`
  - **Exception Message:**
    ```
    {exc_message}
    ```
  - **Traceback:**
    ```
    {tb_str}
    ```
"""
                f.write(red_flag_template)
            
            print(f"Successfully created and appended new requirement {new_req_id} to {REQUIREMENTS_FILE}")

        except Exception as e:
            print(f"FATAL: Could not create Red Flag requirement. Error: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


class WorkflowState:
    def __init__(self, state_file=".workflow_state"):
        self.state_file = Path(state_file)
        self.data = {}
        self._load_state()
        self._ensure_python_executable()

    def _load_state(self):
        if self.state_file.exists():
            with open(self.state_file, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        self.data[key] = value

    def _ensure_python_executable(self):
        if not self.get("PythonExecutablePath") or not Path(self.get("PythonExecutablePath")).exists():
            self.initialize_state()

    def initialize_state(self):
        project_name = os.path.basename(os.getcwd())
        venv_path = Path(os.path.expanduser(f"~/venvs/{project_name}"))
        python_executable_path = venv_path / "bin" / "python"

        if not self.data:
            self.data = {
                "CurrentStage": "Engineer",
                "RequirementPointer": "1",
                "CycleCounter": "1"
            }

        if not python_executable_path.exists():
            print(f"Virtual environment not found at {venv_path}. Creating it now...")
            try:
                venv_path.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["python3", "-m", "venv", str(venv_path)], check=True)
                print("Virtual environment created.")
                print("Installing project in editable mode...")
                subprocess.run([str(python_executable_path), "-m", "pip", "install", "-e", ".[test]"], check=True, cwd=os.getcwd())
                print("Dependencies installed.")
            except subprocess.CalledProcessError as e:
                print(f"Error during environment setup: {e}", file=sys.stderr)
                sys.exit(1)

        self.data["PythonExecutablePath"] = str(python_executable_path)
        self.save()
        print(f"Environment path set to: {python_executable_path}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = str(value)

    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def increment(self, key):
        current_value = int(self.get(key, 0))
        new_value = current_value + 1
        self.set(key, new_value)
        self.save()
        return new_value

    def save(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            for key, value in sorted(self.data.items()):
                f.write(f"{key}={value}\n")
