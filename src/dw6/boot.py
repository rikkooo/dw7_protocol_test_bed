import os
import subprocess
import sys
from pathlib import Path

from dw6.state_manager import WorkflowState


def ensure_environment():
    """
    Ensures that the project's virtual environment is set up correctly.

    This function is idempotent. It checks for the existence of the virtual
    environment and the installation of dependencies, and only performs setup
    actions if they are needed.
    """
    project_root = Path(os.getcwd())
    venv_path = project_root / ".venv"
    state = WorkflowState()

    # 1. Check if the virtual environment exists. If not, create it.
    if not venv_path.exists():
        print("--- Boot: Virtual environment not found. Creating... ---", flush=True)
        try:
            subprocess.run(["uv", "venv"], check=True, capture_output=True, text=True)
            print("--- Boot: Virtual environment created successfully. ---", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"--- Boot: CRITICAL: Failed to create virtual environment. Error: {e.stderr}", file=sys.stderr, flush=True)
            sys.exit(1)

    # 2. Check if the PythonExecutablePath is in the state. If not, set it.
    # This makes the path immutable after first setup.
    if state.get("PythonExecutablePath") is None:
        print("--- Boot: PythonExecutablePath not found in state. Setting... ---", flush=True)
        python_executable_path = venv_path / "bin" / "python"
        state.set("PythonExecutablePath", str(python_executable_path))
        print(f"--- Boot: PythonExecutablePath set to {python_executable_path} ---", flush=True)

    # 3. Check if dependencies are installed. We check for a key marker like pytest.
    # A more robust check could be implemented if needed.
    result = subprocess.run([str(state.get("PythonExecutablePath")), "-m", "pip", "show", "pytest"], capture_output=True, text=True)
    if result.returncode != 0:
        print("--- Boot: Dependencies not installed. Installing... ---", flush=True)
        try:
            # Install the project in editable mode with the 'test' extras.
            subprocess.run(["uv", "pip", "install", "-e", ".[test]"], check=True, capture_output=True, text=True)
            print("--- Boot: Dependencies installed successfully. ---", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"--- Boot: CRITICAL: Failed to install dependencies. Error: {e.stderr}", file=sys.stderr, flush=True)
            sys.exit(1)
