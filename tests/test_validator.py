import unittest
import subprocess
from unittest.mock import patch, MagicMock

from dw6.workflow.validator import ValidatorStage

class TestValidatorStage(unittest.TestCase):

    def setUp(self):
        """Set up a mock state for each test."""
        self.mock_state = MagicMock()
        self.validator_stage = ValidatorStage(self.mock_state)
        self.mock_python_path = "/fake/path/to/python"

    @patch('sys.executable', new='/fake/path/to/python')
    @patch('subprocess.run')
    def test_validate_succeeds(self, mock_run):
        """Test that validate returns True when pytest passes."""
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(self.validator_stage.validate())
        mock_run.assert_called_once_with(
            [self.mock_python_path, "-m", "pytest"], 
            check=True, capture_output=True, text=True
        )

    @patch('sys.executable', new='/fake/path/to/python')
    @patch('subprocess.run')
    def test_validate_fails_on_test_failure(self, mock_run):
        """Test that validate returns False when pytest fails."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'pytest')
        self.assertFalse(self.validator_stage.validate())

    @patch('sys.executable', new='/fake/path/to/python')
    @patch('subprocess.run')
    def test_validate_succeeds_with_failures_allowed(self, mock_run):
        """Test that validate returns True on failure when allow_failures is True."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'pytest')
        self.assertTrue(self.validator_stage.validate(allow_failures=True))

    @patch('sys.executable', new='/fake/path/to/python')
    @patch('subprocess.run')
    def test_validate_fails_on_pytest_error(self, mock_run):
        """Test that validate returns False when pytest itself errors."""
        mock_run.side_effect = subprocess.CalledProcessError(5, 'pytest')
        self.assertFalse(self.validator_stage.validate())

if __name__ == '__main__':
    unittest.main()
