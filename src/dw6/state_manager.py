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
    Enforces the rules and permissions of the DW8 protocol.

    The Governor acts as a security layer, ensuring that all actions performed
    within the workflow adhere to the strict rules defined for each stage.
    It maintains a rule set (`RULES`) that maps each stage to a list of
    permitted commands or actions.

    Before any significant action is executed by the `WorkflowManager`, the
    Governor's `authorize` method is called to verify that the action is
    allowed in the current stage. This prevents unauthorized operations and
    maintains the integrity of the workflow.

    Its methods are loaded dynamically from `src/dw6/st/governor_*.py`.

    Attributes:
        state (WorkflowState): An instance of the workflow state manager.
        current_stage (str): The name of the current workflow stage.
    """
    RULES = {
        "Engineer": [
            "dw6 new",
            "dw6 meta-req",
            "ls",
            "cat",
            "view_file_outline",
            "dw6 approve"
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
            "dw6 approve"
        ],
        "Coder": [
            "replace_file_content",
            "write_to_file",
            "view_file_outline",
            "ls",
            "mkdir",
            "dw6 approve"
        ],
        "Validator": [
            "uv run pytest",
            "dw6 approve"
        ],
        "Deployer": [
            "git add",
            "git commit",
            "git tag",
            "dw6 approve"
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
    The high-level orchestrator for the DW8 workflow.

    The WorkflowManager acts as the central command processor. It receives
    commands from the command-line interface (CLI), interprets them, and
    delegates tasks to the appropriate components. It is the primary entry
    point for user-driven actions like `approve`, `new`, and `status`.

    It coordinates the actions of two key sub-components:
    - Governor: Enforces the rules and permissions for the current workflow stage.
    - WorkflowKernel: Executes the core logic of the workflow, such as advancing
      stages and managing requirement state.

    Like other core components, it uses a dynamic method loading pattern,
    with its methods defined in `src/dw6/st/manager_*.py` files.

    Attributes:
        state (WorkflowState): An instance of the workflow state manager.
        governor (Governor): An instance of the Governor.
        kernel (WorkflowKernel): An instance of the workflow kernel.
        current_stage_name (str): The name of the current workflow stage.
        stage_module (module): The dynamically loaded module for the current stage.
    """
    def __init__(self, state):
        self.state = state
        self.governor = Governor(self.state)
        self.kernel = WorkflowKernel(state)
        self.current_stage_name = self.state.get("CurrentStage")
        self.current_event = None



        # --- Automated Recovery Protocol Briefing ---
        recovery_file = Path(__file__).parent.parent.parent / "docs" / "RECOVERY_PROTOCOL.md"
        if recovery_file.exists():
            print("--- Governor: Recovery Protocol Briefing ---")
            with open(recovery_file, 'r') as f:
                print(f.read())
            print("-------------------------------------------")

        self._load_methods()

        # Ensure the kernel and manager have the latest event details upon initialization
        self.current_event = self.get_current_event_details()
        self.kernel.current_event = self.current_event

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
    Manages the persistent state of the workflow via `workflow_state.json`.

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
