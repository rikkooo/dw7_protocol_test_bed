import os
import sys
from pathlib import Path
from datetime import datetime
from . import config
from . import git_handler
from .templates import TECHNICAL_SPECIFICATION_TEMPLATE

class WorkflowManager:
    def __init__(self):
        self.state = WorkflowState()
        self.current_stage = self.state.get("CurrentStage")

    def start_new_cycle(self, requirement_id):
        self.state.set("CurrentStage", "Engineer")
        self.state.set("RequirementID", requirement_id)
        self.state.set("CycleStartTime", datetime.now().isoformat())
        self.state.save()
        print(f"Starting new development cycle for Requirement ID: {requirement_id}")
        self._run_engineer_stage()

    def approve(self):
        print(f"Attempting to approve stage: {self.current_stage}")
        if self._validate_stage():
            self._advance_stage()
        else:
            print(f"Validation for stage '{self.current_stage}' failed. Cannot advance.", file=sys.stderr)

    def set_stage(self, stage):
        if stage not in config.STAGES:
            print(f"Error: '{stage}' is not a valid stage.", file=sys.stderr)
            return
        self.state.set("CurrentStage", stage)
        self.state.save()
        self.current_stage = stage
        print(f"Workflow stage manually set to: {self.current_stage}")

    def create_new_meta_requirement(self, title, details, priority):
        # Read the existing requirements
        req_file = Path("docs/PROJECT_REQUIREMENTS.md")
        content = req_file.read_text() if req_file.exists() else ""

        # Find the highest existing requirement number
        existing_ids = [int(i) for i in re.findall(r"REQ-DW8-(\d{3})", content)]
        new_id_num = max(existing_ids) + 1 if existing_ids else 1
        new_id = f"REQ-DW8-{new_id_num:03d}"

        # Create the new requirement block
        new_req = f"""---

### ID: {new_id}

- **Title:** {title}
- **Status:** `Pending`
- **Priority:** `{priority}`
- **Details:** {details}
- **SMRs:**
  - [ ] SMR 1

"""
        # Prepend the new requirement to the file
        with open(req_file, "w") as f:
            f.write(new_req + content)
        
        print(f"Successfully created and prioritized new Meta-Requirement: {new_id}")

    def _advance_stage(self):
        current_index = config.STAGES.index(self.current_stage)
        if current_index + 1 < len(config.STAGES):
            self._run_pre_transition_actions()
            next_stage = config.STAGES[current_index + 1]
            self.state.set("CurrentStage", next_stage)
            self.state.save()
            self.current_stage = next_stage
            print(f"Stage advanced to: {self.current_stage}")
            self._reset_failure_counters(self.current_stage)
            self._run_post_transition_actions()
            # Automatically run the next stage's main action
            if self.current_stage == "Researcher":
                self._run_researcher_stage()
            elif self.current_stage == "Coder":
                self._run_coder_stage()
        else:
            self._complete_cycle()

    def _complete_cycle(self):
        cycle_num = int(self.state.get("CycleCounter", 1))
        self.state.set("CycleCounter", cycle_num + 1)
        self.state.set("CurrentStage", "Finished")
        self.state.save()
        print(f"Development cycle {cycle_num} completed.")

    def _increment_failure_counter(self, action_name: str):
        """Increments a failure counter for a specific action."""
        stage = self.current_stage
        counter_key = f"FailureCounters.{stage}.{action_name}"
        current_count = int(self.state.get(counter_key, 0))
        new_count = current_count + 1
        self.state.set(counter_key, str(new_count))
        self.state.save()
        print(f"Failure counter for '{action_name}' in stage '{stage}' incremented to {new_count}.", file=sys.stderr)

    def _reset_failure_counters(self, stage: str):
        """Resets all failure counters for a given stage."""
        keys_to_remove = []
        prefix = f"FailureCounters.{stage}."
        for key in self.state.data:
            if key.startswith(prefix):
                keys_to_remove.append(key)
        
        if not keys_to_remove:
            return

        for key in keys_to_remove:
            del self.state.data[key]
        
        self.state.save()
        print(f"All failure counters for stage '{stage}' have been reset.")

    def _validate_stage(self):
        stage_validator_map = {
            "Engineer": self._validate_engineer,
            "Researcher": self._validate_researcher,
            "Coder": self._validate_coder,
            "Validator": self._validate_validator,
            "Deployer": self._validate_deployment
        }
        validator = stage_validator_map.get(self.current_stage)
        if validator:
            return validator()
        return False

    # --- Stage-specific methods ---

    def _run_engineer_stage(self):
        req_id = self.state.get("RequirementID")
        spec_path = Path(f"deliverables/tech_specs/SPEC_{req_id}.md")
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        spec_content = TECHNICAL_SPECIFICATION_TEMPLATE.format(
            title=f"Spec for {req_id}",
            req_id=req_id,
            date=datetime.now().strftime("%Y-%m-%d")
        )
        with open(spec_path, "w") as f:
            f.write(spec_content)
        print(f"Generated technical specification skeleton at: {spec_path}")

    def _validate_engineer(self):
        req_id = self.state.get("RequirementID")
        spec_path = Path(f"deliverables/tech_specs/SPEC_{req_id}.md")
        if not spec_path.exists() or os.path.getsize(spec_path) < 100:
            print(f"Validation failed: Tech spec {spec_path} is missing or incomplete.", file=sys.stderr)
            return False
        print("Engineer stage validated: Tech spec is present and not empty.")
        return True

    def _run_researcher_stage(self):
        req_id = self.state.get("RequirementID")
        research_path = Path(f"deliverables/research/cycle_{self.state.get('CycleCounter')}_research_report.md")
        research_path.parent.mkdir(parents=True, exist_ok=True)
        with open(research_path, "w") as f:
            f.write(f"# Research Report for {req_id}\n\n*AI-generated research notes will go here.*
")
        print(f"Generated research report skeleton at: {research_path}")

    def _validate_researcher(self):
        research_path = Path(f"deliverables/research/cycle_{self.state.get('CycleCounter')}_research_report.md")
        if not research_path.exists() or os.path.getsize(research_path) < 50:
            print(f"Validation failed: Research report {research_path} is missing or incomplete.", file=sys.stderr)
            return False
        print("Researcher stage validated: Research report is present and not empty.")
        return True

    def _run_coder_stage(self):
        print("Coder stage started. Waiting for code implementation.")
        # In a real workflow, this is where the AI would write code.

    def _validate_coder(self):
        # For now, we'll just check if the src directory has been modified recently.
        # This is a placeholder for a more robust check, like running a linter.
        src_path = Path("src")
        if not any(f.stat().st_mtime > self.state.get_as_datetime("CycleStartTime").timestamp() for f in src_path.glob("**/*") if f.is_file()):
            print("Validation failed: No code changes detected in src directory.", file=sys.stderr)
            return False
        print("Coder stage validated: Code changes detected.")
        return True

    def _generate_coder_deliverable(self):
        """Generates a deliverable for the Coder stage."""
        deliverable_path = Path(f"deliverables/coder/cycle_{self.state.get('CycleCounter')}_summary.md")
        deliverable_path.parent.mkdir(parents=True, exist_ok=True)
        
        commit_sha = git_handler.get_latest_commit_sha()
        status = git_handler.get_git_status()

        content = f"""# Coder Stage Summary

- **Cycle:** {self.state.get('CycleCounter')}
- **Final Commit SHA:** `{commit_sha}`

## Git Status

```
{status}
```
"""
        with open(deliverable_path, "w") as f:
            f.write(content)
        print(f"Generated coder deliverable at: {deliverable_path}")

    def _validate_validator(self):
        # Placeholder for running tests.
        print("Validator stage validated: Tests would be run here.")
        return True

    def _validate_deployment(self, allow_failures=False):
        """
        Validates the deployment by pushing the code to the remote repository and tagging it.
        This uses the MCP-based git handler functions.
        """
        print("Validating deployment...")

        # Push the source and test files first.
        # This will be a call to the real mcp_push_files in the Coder stage.
        commit_sha = git_handler.mcp_push_files("feat: Coder stage submission", ["src", "tests"])

        if not commit_sha:
            print("Deployment validation failed: Could not push files via MCP.", file=sys.stderr)
            self._increment_failure_counter("mcp_push_files")
            if not allow_failures:
                sys.exit(1)
            return False

        # Now, create and push the tag for the new commit.
        cycle = self.state.get("CycleCounter", "1")
        tag_name = f"v1.{cycle}"
        git_handler.mcp_create_and_push_tag(tag_name, commit_sha, f"Release for cycle {cycle}")

        print(f"Deployment validation successful: Commit {commit_sha[:7]} was pushed and tagged as {tag_name}.")
        return True

    def _run_pre_transition_actions(self):
        pass

    def _run_post_transition_actions(self):
        if self.current_stage == "Validator":
            git_handler.save_current_commit_sha()
            self._generate_coder_deliverable()


class WorkflowState:
    def __init__(self):
        self.state_file = Path("logs/workflow_state.txt")
        self.data = {}
        if self.state_file.exists():
            with open(self.state_file, "r") as f:
                for line in f:
                    key, value = line.strip().split("=", 1)
                    self.data[key] = value
        else:
            self.initialize_state()

    def initialize_state(self):
        self.data = {
            "CurrentStage": "Engineer",
            "RequirementPointer": "1",
            "CycleCounter": "1"
        }
        self.save()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = str(value)

    def save(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            for key, value in self.data.items():
                f.write(f"{key}={value}\n")
