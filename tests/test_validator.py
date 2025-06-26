import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dw6.state_manager import WorkflowManager

class TestValidatorStage(unittest.TestCase):

    @patch('dw6.state_manager.subprocess.run')
    @patch('dw6.state_manager.subprocess.check_output')
    def test_validator_fails_with_pytest_error(self, mock_check_output, mock_run):
        """Test that validation fails if pytest itself fails (e.g., no tests found)."""
        # Arrange
        # Pytest exits with code 5 if no tests are collected.
        # This will cause check_output to raise a CalledProcessError.
        mock_check_output.side_effect = subprocess.CalledProcessError(5, 'pytest')
        manager = WorkflowManager()
        manager.current_stage = 'Validator'

        # Act
        result = manager._validate_tests()

        # Assert
        self.assertFalse(result)
        mock_run.assert_not_called() # The main test run should not happen

    @patch('dw6.state_manager.subprocess.run')
    @patch('dw6.state_manager.subprocess.check_output')
    def test_validator_fails_on_test_failure(self, mock_check_output, mock_run):
        """Test that the Validator stage fails if pytest tests fail."""
        # Arrange
        mock_check_output.return_value = 'collected 1 item'.encode('utf-8')
        # subprocess.run with check=True will raise CalledProcessError on non-zero exit code
        mock_run.side_effect = subprocess.CalledProcessError(1, 'pytest')
        manager = WorkflowManager()
        manager.current_stage = 'Validator'

        # Act
        result = manager._validate_tests()

        # Assert
        self.assertFalse(result)
        mock_check_output.assert_called_once()
        mock_run.assert_called_once()

    @patch('dw6.state_manager.subprocess.run')
    @patch('dw6.state_manager.subprocess.check_output')
    def test_validator_succeeds_with_tests(self, mock_check_output, mock_run):
        """Test that the Validator stage succeeds when tests are found and pass."""
        # Arrange
        mock_check_output.return_value = 'collected 1 item'.encode('utf-8')
        mock_run.return_value = MagicMock(returncode=0) # Success
        manager = WorkflowManager()
        manager.current_stage = 'Validator'

        # Act
        result = manager._validate_tests()

        # Assert
        self.assertTrue(result)
        mock_check_output.assert_called_once()
        mock_run.assert_called_once()

    @patch('dw6.state_manager.subprocess.run')
    @patch('dw6.state_manager.subprocess.check_output')
    def test_validator_succeeds_with_failures_when_allowed(self, mock_check_output, mock_run):
        """Test that validation succeeds with test failures if allow_failures is True."""
        # Arrange
        mock_check_output.return_value = 'collected 1 item'.encode('utf-8')
        mock_run.side_effect = subprocess.CalledProcessError(1, 'pytest')
        manager = WorkflowManager()
        manager.current_stage = 'Validator'

        # Act
        result = manager._validate_tests(allow_failures=True)

        # Assert
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
