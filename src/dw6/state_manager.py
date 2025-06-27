import re
import sys
import os
import subprocess
import shutil
import git
import traceback
from pathlib import Path
from datetime import datetime, timezone

from dw6.workflow.kernel import WorkflowKernel
from dw6.workflow.engineer import EngineerStage
from dw6.workflow.researcher import ResearcherStage
from dw6.workflow.coder import CoderStage
from dw6.workflow.validator import ValidatorStage
from dw6.workflow.deployer import DeployerStage
from dw6.workflow.rehearsal import RehearsalStage

MASTER_FILE = "docs/WORKFLOW_MASTER.md"
REQUIREMENTS_FILE = "docs/PROJECT_REQUIREMENTS.md"
APPROVAL_FILE = "logs/approvals.log"
FAILURE_THRESHOLD = 3
STAGES = ["Engineer", "Researcher", "Coder", "Validator", "Deployer", "Rehearsal"]
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
            print(f"--- Governor: Command '{command}' is not authorized in the '{self.current_stage}' stage. ---", file=sys.stderr)
            return False
        return True

class WorkflowManager:
    def __init__(self, state):
        self.state = state
        self.governor = Governor(self.state)
        self.kernel = WorkflowKernel(state)
        self.current_stage_name = self.state.get("CurrentStage")
        self.stage_module = self._load_stage_module()

    def _load_stage_module(self):
        stage_classes = {
            "Engineer": EngineerStage,
            "Researcher": ResearcherStage,
            "Coder": CoderStage,
            "Validator": ValidatorStage,
            "Deployer": DeployerStage,
            "Rehearsal": RehearsalStage,
        }
        stage_class = stage_classes.get(self.current_stage_name)
        if not stage_class:
            raise ValueError(f"Unknown stage: {self.current_stage_name}")
        return stage_class(self.state)

    def approve(self, needs_research=False, allow_failures=False):
        print(f"--- Governor: Attempting to approve stage {self.current_stage_name}... ---")
        try:
            if self.current_stage_name == "Coder":
                self.kernel.save_current_commit_sha()

            if self.stage_module.validate(allow_failures=allow_failures):
                # On success, reset the default counter and advance.
                # Validator resets its own 'pytest' counter within its own method.
                self.state.reset_failure_counter(self.current_stage_name, 'default')
                self.kernel.advance_stage(needs_research)
            else:
                # On validation failure, raise exception to be handled by the except block.
                raise Exception("Stage exit criteria not met.")
        except Exception as e:
            print(f"--- Governor: Stage {self.current_stage_name} Approval Failed. ---", file=sys.stderr)
            
            # Increment the default counter for non-validator stages.
            if self.current_stage_name != 'Validator':
                self.state.increment_failure_counter(self.current_stage_name, 'default')

            # Check the relevant counter against the threshold.
            counter_name = 'pytest' if self.current_stage_name == 'Validator' else 'default'
            if self.state.get_failure_counter(self.current_stage_name, counter_name) >= FAILURE_THRESHOLD:
                print(f"--- Governor: Failure threshold reached for {self.current_stage_name}.{counter_name}. Entering Rehearsal. ---", file=sys.stderr)
                self.state.set("PreviousStage", self.current_stage_name) # Store where we came from
                self.state.set("CurrentStage", "Rehearsal")
                self.state.save()
            else:
                # Original halt logic
                print(f"Error: {e}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                self.kernel._handle_failure(e)
                print(f"--- Governor: Stage {self.current_stage_name} Approval Failed. Halting. ---", file=sys.stderr)

import json

class WorkflowState:
    def __init__(self, state_file="data/workflow_state.json"):
        self.state_file = Path(state_file)
        self.data = {}
        self.load()

    def load(self):
        # One-time migration from old format
        old_state_file = Path('.workflow_state')
        if old_state_file.exists() and not self.state_file.exists():
            print(f"--- Governor: Migrating state from {old_state_file} to {self.state_file} ---")
            temp_data = {}
            with open(old_state_file, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        temp_data[key] = value
            self.data = temp_data
            self.save()
            old_state_file.unlink() # Remove old file after successful migration
            return

        if self.state_file.exists() and self.state_file.stat().st_size > 0:
            try:
                with open(self.state_file, "r") as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                print(f"--- Governor: WARNING: Could not decode JSON from {self.state_file}. Re-initializing. ---", file=sys.stderr)
                self.initialize_state()
        else:
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

    def get_failure_counter(self, stage, counter_name="default"):
        key = f"FailureCounters.{stage}.{counter_name}"
        return int(self.get(key, 0))

    def increment_failure_counter(self, stage, counter_name="default"):
        key = f"FailureCounters.{stage}.{counter_name}"
        current_value = self.get_failure_counter(stage, counter_name)
        new_value = current_value + 1
        self.set(key, new_value)
        self.save()
        print(f"--- Governor: Failure counter {stage}.{counter_name} incremented to {new_value}. ---")
        return new_value

    def reset_failure_counter(self, stage, counter_name="default"):
        key = f"FailureCounters.{stage}.{counter_name}"
        if self.get(key) is not None:
            self.set(key, 0)
            self.save()
            print(f"--- Governor: Failure counter {stage}.{counter_name} reset to 0. ---")

    def save(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(self.data, f, indent=2, sort_keys=True)
