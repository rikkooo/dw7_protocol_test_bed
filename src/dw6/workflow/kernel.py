import importlib
import os
import sys
from pathlib import Path
from types import MethodType

class WorkflowKernel:
    """
    The core engine of the DW8 workflow.

    The WorkflowKernel is the heart of the system, responsible for executing the
    fundamental logic of the development workflow. It is designed as a lean,
    dynamically-loaded interface that orchestrates state transitions, processes
    events, handles failures, and manages the overall lifecycle of a development
    task according to the DW8 protocol.

    Its modular design is a key feature. All of its operational methods (e.g.,
    `advance_stage`, `load_current_event_details`, `_handle_failure`) are
    defined in individual files within the `src/dw6/workflow/kr/` subdirectory.
    This isolates logic, enhances maintainability, and aligns with the Prism
    Protocol's goal of context stability.

    Attributes:
        state (WorkflowState): An instance of the workflow state manager.
        current_event (dict): The event currently being processed.
        current_stage (str): The name of the current workflow stage.
        python_executable_path (str): The path to the Python executable in the
                                      active virtual environment.
    """
    def __init__(self, state):
        self.state = state
        self.current_event = None  # Initialize to None

        # Dynamically load all methods from the 'kr' subdirectory
        self._load_methods()

        # --- Core Initialization Sequence ---
        # The following methods are dynamically loaded.

        # 1. Manage user profile and session data
        self._manage_user_profile()

        # 2. Display personalized startup greeting and status
        self._display_startup_summary()

        # 3. Ensure environment variables are set (e.g., GITHUB_TOKEN)
        self._load_environment()

        # 4. Set core attributes from the state
        self.current_stage = self.state.get("CurrentStage")
        self.python_executable_path = self.state.get("PythonExecutablePath")

        # 5. Load the details of the current requirement pointed to by the state
        self.load_current_event_details()

    def _load_methods(self):
        """
        Dynamically discovers and binds methods from the 'kr' subdirectory.
        
        Each .py file in 'kr' is expected to contain a single function
        with the same name as the file. This function is loaded and bound
        to the kernel instance as a method.
        """
        kernel_methods_dir = Path(__file__).parent / "kr"
        for f in kernel_methods_dir.glob("*.py"):
            if f.name == "__init__.py":
                continue
            
            method_name = f.stem
            module_path = f"dw6.workflow.kr.{method_name}"
            
            try:
                module = importlib.import_module(module_path)
                method_function = getattr(module, method_name)
                # Bind the function to the instance, making it a method
                setattr(self, method_name, MethodType(method_function, self))
            except (ImportError, AttributeError) as e:
                print(f"--- Governor: CRITICAL: Failed to load kernel method '{method_name}' from '{module_path}'. Error: {e} ---", file=sys.stderr)
                # Depending on the desired robustness, you might want to exit here
                # sys.exit(1)
