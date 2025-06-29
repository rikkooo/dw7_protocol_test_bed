import importlib
import os
import sys
from pathlib import Path
from types import MethodType

# Import kernel as it's a dependency for WorkflowManager
from dw6.workflow.kernel import WorkflowKernel

# --- Constants and Definitions ---
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
    """
    The Governor enforces the rules of the DW8 protocol, ensuring that
    only authorized actions are performed in each stage of the workflow.
    """
    RULES = {
        "Engineer": [
            "uv run dw6 new",
            "uv run dw6 meta-req",
            "ls",
            "cat",
            "view_file_outline",
            "uv run dw6 approve"
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
            "uv run dw6 approve"
        ],
        "Coder": [
            "replace_file_content",
            "write_to_file",
            "view_file_outline",
            "ls",
            "mkdir",
            "uv run dw6 approve"
        ],
        "Validator": [
            "uv run pytest",
            "uv run dw6 approve"
        ],
        "Deployer": [
            "git add",
            "git commit",
            "git tag",
            "uv run dw6 approve"
        ]
    }

    def __init__(self, state):
        self.state = state
        self.current_stage = self.state.get("CurrentStage")
        self._load_methods()

    def _load_methods(self):
        methods_dir = Path(__file__).parent / "st"
        # The Governor only has one method to load currently
        f = methods_dir / "governor_authorize.py"
        if f.exists():
            method_name = "authorize"
            module_path = f"dw6.st.{f.stem}"
            try:
                module = importlib.import_module(module_path)
                method_function = getattr(module, method_name)
                setattr(self, method_name, MethodType(method_function, self))
            except (ImportError, AttributeError) as e:
                print(f"--- Governor: CRITICAL: Failed to load Governor method '{method_name}'. Error: {e} ---", file=sys.stderr)


class WorkflowManager:
    """
    The WorkflowManager is the high-level orchestrator. It interprets user
    commands and directs the WorkflowKernel and Stage modules to execute
    the appropriate actions.
    """
    def __init__(self, state):
        self.state = state
        self.governor = Governor(self.state)
        self.kernel = WorkflowKernel(state, self.state.get("PendingEvents", []))
        self.current_stage_name = self.state.get("CurrentStage")
        self._load_methods()
        # This must be called after its own method is loaded
        self.stage_module = self._load_stage_module()

    def _load_methods(self):
        methods_dir = Path(__file__).parent / "st"
        for f in methods_dir.glob("manager_*.py"):
            # Replace double underscore with single for private methods
            method_name = f.stem.replace("manager_", "").replace("__", "_")
            module_path = f"dw6.st.{f.stem}"
            try:
                module = importlib.import_module(module_path)
                # The function name inside the module is the method_name
                method_function = getattr(module, method_name)
                setattr(self, method_name, MethodType(method_function, self))
            except (ImportError, AttributeError) as e:
                print(f"--- Governor: CRITICAL: Failed to load Manager method '{method_name}'. Error: {e} ---", file=sys.stderr)


class WorkflowState:
    """
    The WorkflowState class manages the persistent state of the workflow,
    reading from and writing to the `workflow_state.json` file.
    """
    def __init__(self, state_file="data/workflow_state.json"):
        self.state_file = Path(state_file)
        self.data = {}
        self._load_methods()
        # The `load` method, now dynamically loaded, initializes the state
        self.load()


    def _load_methods(self):
        methods_dir = Path(__file__).parent / "st"
        for f in methods_dir.glob("*.py"):
            # Exclude __init__ and methods prefixed for other classes
            if f.name.startswith(("__", "governor_", "manager_")):
                continue
            
            method_name = f.stem
            module_path = f"dw6.st.{method_name}"
            try:
                module = importlib.import_module(module_path)
                method_function = getattr(module, method_name)
                setattr(self, method_name, MethodType(method_function, self))
            except (ImportError, AttributeError) as e:
                print(f"--- Governor: CRITICAL: Failed to load State method '{method_name}'. Error: {e} ---", file=sys.stderr)
