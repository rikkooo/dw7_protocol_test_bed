import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open, call
import unittest

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dw6.state_manager import WorkflowState, WorkflowManager

class TestWorkflowStateInitialization(unittest.TestCase):


    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.run')
    @patch('pathlib.Path.mkdir')
    @patch('os.path.basename')
    @patch('pathlib.Path.exists')
    def test_state_initialization_creates_env_and_persists_path(self, mock_exists, mock_basename, mock_mkdir, mock_run, mock_file):
        """Verify that WorkflowState creates venv and persists the path on first run."""
        # Arrange
        mock_basename.return_value = "dw7_protocol_test_bed"
        # 1st call to exists() is for the state file (False = new project)
        # 2nd call is for the python executable (False = venv needs creation)
        mock_exists.return_value = False 

        # Act
        state = WorkflowState()

        # Assert
        project_name = "dw7_protocol_test_bed"
        venv_path = Path(os.path.expanduser(f"~/venvs/{project_name}"))
        python_executable_path = venv_path / "bin" / "python"

        expected_calls = [
            call(["uv", "venv", str(venv_path)], check=True),
            call(["uv", "pip", "install", "-e", ".[test]"], check=True, cwd=os.getcwd())
        ]
        mock_run.assert_has_calls(expected_calls, any_order=False)
        mock_mkdir.assert_any_call(parents=True, exist_ok=True)
        self.assertEqual(state.get("PythonExecutablePath"), str(python_executable_path))


if __name__ == '__main__':
    unittest.main()
