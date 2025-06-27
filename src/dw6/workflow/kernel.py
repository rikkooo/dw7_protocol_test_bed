import re
import sys
import os
import traceback
import git
from pathlib import Path
from datetime import datetime, timezone

# Assuming these constants will be moved to a central config or are accessible
REQUIREMENTS_FILE = "docs/PROJECT_REQUIREMENTS.md"
FAILURE_THRESHOLD = 3
STAGES = ["Engineer", "Researcher", "Coder", "Validator", "Deployer", "Rehearsal"]

class WorkflowKernel:
    def __init__(self, state):
        self.state = state
        self.current_stage = self.state.get("CurrentStage")
        self.python_executable_path = self.state.get("PythonExecutablePath")

    def advance_stage(self, needs_research=False):
        self._reset_failure_counters(self.current_stage)

        # Explicit state transitions are more robust than index-based logic.
        if self.current_stage == "Rehearsal":
            next_stage = self.state.get("PreviousStage")
            self.state.delete("PreviousStage") # Clean up state
            if not next_stage:
                print("--- Governor: WARNING: PreviousStage not found. Defaulting to Engineer. ---", file=sys.stderr)
                next_stage = "Engineer"
        elif self.current_stage == "Engineer":
            next_stage = "Researcher" if needs_research else "Coder"
        elif self.current_stage == "Researcher":
            next_stage = "Coder"
        elif self.current_stage == "Coder":
            next_stage = "Validator"
        elif self.current_stage == "Validator":
            next_stage = "Deployer"
        elif self.current_stage == "Deployer":
            next_stage = "Engineer"
        else:
            raise Exception(f"Unknown stage transition from {self.current_stage}")

        self.state.set("CurrentStage", next_stage)
        if next_stage == "Engineer":
            self.state.increment("CycleCounter")
            self._advance_requirement_pointer()
            self._perform_context_refresh()
        self.state.save()
        print(f"--- Governor: Stage advanced from {self.current_stage} to {next_stage}. ---")

    def _handle_failure(self, exception):
        failure_key, current_failure_count = self._get_failure_context()
        
        if current_failure_count >= FAILURE_THRESHOLD:
            print(f"--- Governor: Failure threshold reached for {failure_key}. Escalating... ---", file=sys.stderr)
            new_req_id = self._create_red_flag_requirement(exception)
            if new_req_id:
                self.state.set("RequirementPointer", new_req_id)
                self.state.set("CurrentStage", "Engineer")
                self._reset_failure_counters(self.current_stage)
                self.state.save()
                print(f"--- Governor: Workflow reset to Engineer stage. Focus is now on {new_req_id}. ---")
            else:
                print("--- Governor: FATAL ERROR during escalation. Workflow halted. ---", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"--- Governor: Stage {self.current_stage} Approval Failed. Halting. ---", file=sys.stderr)

    def _get_failure_context(self):
        stage = self.current_stage
        failure_key = f"FailureCounters.{stage}.default"
        current_failure_count = self.state.increment(failure_key)
        return failure_key, current_failure_count

    def _reset_failure_counters(self, stage):
        # Simplified for now, can be expanded
        self.state.set(f"FailureCounters.{stage}.default", 0)
        self.state.save()

    def save_current_commit_sha(self):
        try:
            repo = git.Repo(search_parent_directories=True)
            self.state.set("Validator_CommitSHA", repo.head.commit.hexsha)
            self.state.save()
        except Exception as e:
            print(f"Error saving commit SHA: {e}", file=sys.stderr)

    def _advance_requirement_pointer(self):
        try:
            with open(REQUIREMENTS_FILE, "r") as f:
                lines = f.readlines()

            # Find the first line that contains '[P]' for 'Pending'
            for line in lines:
                if line.strip().startswith('[P]'):
                    req_id_match = re.search(r'\[(REQ-DW8-\d+)\]', line)
                    if req_id_match:
                        req_id = req_id_match.group(1)
                        self.state.set("RequirementPointer", req_id)
                        self.state.save()
                        print(f"--- Governor: RequirementPointer set to first pending requirement: {req_id}. ---")
                        return
            
            print("--- Governor: No pending requirements found. ---")

        except Exception as e:
            print(f"Error advancing requirement pointer: {e}", file=sys.stderr)

    def _perform_context_refresh(self):
        print("\n--- Governor: Performing Mandatory Context Refresh ---")
        try:
            active_req_id = self.state.get("RequirementPointer")
            if not active_req_id:
                print("--- Governor: No active requirement pointer found. Cannot refresh context. ---", file=sys.stderr)
                return

            req_file_path = f"docs/reqs/{active_req_id}.md"
            print(f"\n*** Active Requirement ({active_req_id}) ***")
            if os.path.exists(req_file_path):
                with open(req_file_path, "r") as f:
                    print(f.read())
            else:
                print(f"--- Governor: Requirement file not found: {req_file_path} ---", file=sys.stderr)

            tutorial_file = "docs/AI_PROTOCOL_TUTORIAL.md"
            if os.path.exists(tutorial_file):
                print(f"\n*** AI Protocol Tutorial ({os.path.basename(tutorial_file)}) ***")
                with open(tutorial_file, "r") as f:
                    print(f.read())
            print("\n--- Context Refresh Complete ---\n")
        except Exception as e:
            print(f"Error during context refresh: {e}", file=sys.stderr)

    def _create_red_flag_requirement(self, exception):
        try:
            # Determine the next requirement ID
            with open(REQUIREMENTS_FILE, "r") as f:
                content = f.read()
            req_ids = [int(num) for num in re.findall(r'REQ-DW8-(\d+)', content)]
            next_id = max(req_ids) + 1 if req_ids else 1
            new_req_id = f"REQ-DW8-{next_id:03d}"

            # Create the detailed red flag requirement file
            red_flag_path = f"docs/reqs/{new_req_id}.md"
            exc_type = type(exception).__name__
            exc_message = str(exception).replace('\n', '\n    ')
            tb_str = "".join(traceback.format_tb(exception.__traceback__)).replace('\n', '\n      ')

            red_flag_content = f"""### ID: {new_req_id}

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
            with open(red_flag_path, "w") as f:
                f.write(red_flag_content)
            print(f"Successfully created red flag file: {red_flag_path}")

            # Prepend the new requirement to the master index to give it top priority
            new_index_line = f"[P] [C] [{new_req_id}] Red Flag: Unhandled Critical Failure in {self.current_stage} Stage -> ./reqs/{new_req_id}.md\n"
            with open(REQUIREMENTS_FILE, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write(new_index_line + content)
            print(f"Successfully prepended {new_req_id} to {REQUIREMENTS_FILE}")

            return new_req_id

        except Exception as e:
            print(f"FATAL: Could not create Red Flag requirement. Error: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return None

