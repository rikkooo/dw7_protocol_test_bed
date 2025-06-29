import unittest
import json
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta

# Mock the kernel and its dependencies for standalone testing
class MockState:
    def __init__(self):
        self.data = {
            "RequirementPointer": "REQ-TEST-001",
            "CurrentStage": "Coder"
        }
    def get(self, key, default=None):
        return self.data.get(key, default)

class MockKernel:
    def __init__(self):
        self.state = MockState()
        # Dynamically import and bind the methods to the mock kernel instance
        from dw6.workflow.kr._manage_user_profile import _manage_user_profile
        from dw6.workflow.kr._display_startup_summary import _display_startup_summary
        self._manage_user_profile = _manage_user_profile.__get__(self)
        self._display_startup_summary = _display_startup_summary.__get__(self)

class TestKernelPersonalization(unittest.TestCase):

    def setUp(self):
        self.kernel = MockKernel()

    def test_manage_user_profile_first_run(self):
        """Test profile creation on the first run."""
        mock_sys = MagicMock()
        mock_sys.modules = {}
        with patch('dw6.workflow.kr._manage_user_profile.sys', mock_sys), \
             patch('builtins.input', return_value='Riko') as mock_input, \
             patch('pathlib.Path.exists', return_value=False), \
             patch('builtins.open', mock_open()) as mock_file_open, \
             patch('dw6.workflow.kr._manage_user_profile.json') as mock_json:

            self.kernel._manage_user_profile()

            mock_input.assert_called_once()
            mock_file_open.assert_called_once_with(unittest.mock.ANY, 'w')
            self.assertEqual(self.kernel.user_profile['user_name'], 'Riko')
            self.assertTrue('last_session_timestamp' in self.kernel.user_profile)
            mock_json.dump.assert_called_once()

    def test_manage_user_profile_existing_user(self):
        """Test loading an existing user profile."""
        mock_sys = MagicMock()
        mock_sys.modules = {}
        profile_content = {'user_name': 'Riko', 'last_session_timestamp': '2023-01-01T12:00:00'}
        with patch('dw6.workflow.kr._manage_user_profile.sys', mock_sys), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open()), \
             patch('dw6.workflow.kr._manage_user_profile.json') as mock_json:

            mock_json.load.return_value = profile_content
            self.kernel._manage_user_profile()

            mock_json.load.assert_called_once()
            self.assertEqual(self.kernel.user_profile['user_name'], 'Riko')
            self.assertNotEqual(self.kernel.user_profile['last_session_timestamp'], '2023-01-01T12:00:00')
            mock_json.dump.assert_called_once()

    @patch('builtins.print')
    def test_display_startup_summary(self, mock_print):
        """Test the startup summary display."""
        self.kernel.user_profile = {
            'user_name': 'Riko',
            'last_session_timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
        }
        self.kernel._display_startup_summary()

        # Check for key phrases in the output
        mock_print.assert_any_call("\n--- DW8 Workflow Initialized ---")
        mock_print.assert_any_call("Welcome back, Riko. Your last session was 2 hours ago.")
        mock_print.assert_any_call("Active Requirement: REQ-TEST-001")
        mock_print.assert_any_call("Current Stage: Coder")

if __name__ == '__main__':
    unittest.main()
