import unittest
import os
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from dw6.state_manager import WorkflowManager, WorkflowState

class TestWorkflowManagerIntegration(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('dw6.state_manager.WorkflowState')
        self.mock_WorkflowState = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @patch('dw6.workflow.kernel.WorkflowKernel._handle_failure')
    def test_failure_counter_and_rehearsal_transition(self, mock_handle_failure):
        mock_state_instance = self.mock_WorkflowState.return_value
        mock_state_instance.get.return_value = 'Validator'
        manager = WorkflowManager(mock_state_instance)

        # --- Test Case 1: Failure count BELOW threshold ---
        mock_state_instance.get_failure_counter.return_value = 2
        with patch('dw6.workflow.validator.ValidatorStage.validate', return_value=False):
            manager.approve()

        # Check that the failure was handled, but not escalated to rehearsal
        mock_handle_failure.assert_called_once()
        # In this specific failure path for the Validator, `set` is not called by the approve method's exception handler.
        mock_state_instance.set.assert_not_called()

        # --- Reset mocks for the next test case ---
        mock_handle_failure.reset_mock()
        mock_state_instance.set.reset_mock()

        # --- Test Case 2: Failure count AT threshold ---
        mock_state_instance.get_failure_counter.return_value = 3
        with patch('dw6.workflow.validator.ValidatorStage.validate', return_value=False):
            manager.approve()

        # Check that we transitioned to the Rehearsal stage and did not call the old handler
        mock_state_instance.set.assert_any_call('CurrentStage', 'Rehearsal')
        mock_handle_failure.assert_not_called()

    def test_engineer_to_researcher_transition(self):
        mock_state_instance = self.mock_WorkflowState.return_value
        mock_state_instance.get.return_value = 'Engineer'
        manager = WorkflowManager(mock_state_instance)

        with patch('dw6.workflow.engineer.EngineerStage.validate', return_value=True):
            manager.approve(needs_research=True)

        mock_state_instance.set.assert_called_with('CurrentStage', 'Researcher')

    @patch('dw6.workflow.engineer.EngineerStage.validate', return_value=True)
    def test_engineer_to_coder_transition(self, mock_validate):
        mock_state_instance = self.mock_WorkflowState.return_value
        mock_state_instance.get.return_value = 'Engineer'
        manager = WorkflowManager(mock_state_instance)

        manager.approve(needs_research=False)

        mock_validate.assert_called_once()
        mock_state_instance.set.assert_called_with('CurrentStage', 'Coder')

    def test_researcher_to_coder_transition(self):
        mock_state_instance = self.mock_WorkflowState.return_value
        mock_state_instance.get.return_value = 'Researcher'
        manager = WorkflowManager(mock_state_instance)

        with patch('dw6.workflow.researcher.ResearcherStage.validate', return_value=True):
            manager.approve()

        mock_state_instance.set.assert_called_with('CurrentStage', 'Coder')

    def test_create_new_requirement_json(self):
        mock_state_instance = self.mock_WorkflowState.return_value
        mock_state_instance.get.return_value = 'Engineer'  # Set a default stage
        manager = WorkflowManager(mock_state_instance)

        req_id = "REQ-DW8-TEST-001"
        title = "Test JSON Requirement"
        description = "This is a test description."
        acceptance_criteria = ["Criterion 1", "Criterion 2"]

        # Mock the file system
        m = mock_open()
        with patch("builtins.open", m):
            with patch("pathlib.Path.exists", return_value=False):
                with patch("pathlib.Path.mkdir"):
                    manager.create_new_requirement(req_id, title, description, acceptance_criteria)

        # Verify the event file was created correctly
        event_file_path = Path(f"events/{req_id}.json")
        m.assert_any_call(event_file_path, "w", encoding='utf-8')

        # Verify the pending events queue was updated (testing the creation path)
        pending_file_path = "data/pending_events.json"
        # The code opens this file for 'r+' first, then 'w' in the except block.
        # We will check the 'w' call which happens when the file doesn't exist, as mocked.
        m.assert_any_call(pending_file_path, "w")

if __name__ == '__main__':
    unittest.main()
