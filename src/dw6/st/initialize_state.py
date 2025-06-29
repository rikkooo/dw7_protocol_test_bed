import os
import subprocess
import sys
from pathlib import Path

def initialize_state(self):
    print("--- Governor: Initializing new workflow state. ---")
    # REQ-DW8-017-02: Automate Virtual Environment Setup
    project_name = os.path.basename(os.getcwd())
    venv_path = Path(os.path.expanduser(f"~/venvs/{project_name}"))
    python_executable_path = venv_path / "bin" / "python"

    if not self.data:
        self.data = {
            "CurrentStage": "Engineer",
            "RequirementPointer": "1",
            "CycleCounter": "1",
            "PendingEvents": [],
            "CognitiveCheckpoint": "Riko",
        "statistics": {
            "total_requirements_completed": 0,
            "total_requirements_pending": 0,
            "failure_rates_by_stage": {}
        }
    }

    if not python_executable_path.exists():
        print(f"Virtual environment not found at {venv_path}. Creating it now...")
        try:
            venv_path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["uv", "venv", str(venv_path)], check=True)
            print("Virtual environment created.")
            print("Installing project in editable mode...")
            subprocess.run(["uv", "pip", "install", "-e", ".[test]"], check=True, cwd=os.getcwd())
            print("Dependencies installed.")
        except subprocess.CalledProcessError as e:
            print(f"Error during environment setup: {e}", file=sys.stderr)
            sys.exit(1)

    self.data["PythonExecutablePath"] = str(python_executable_path)
    self.save()
    print(f"Environment path set to: {python_executable_path}")
