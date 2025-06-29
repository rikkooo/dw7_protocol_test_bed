from unittest.mock import patch, MagicMock
from dw6.state_manager import WorkflowManager

def tvte(self):
    """
    Tests the transition from the Validator to the Engineer stage with a stateful mock.
    """
    # --- Create a stateful mock --- 
    mock_state_instance = self.mock_WorkflowState.return_value
    mock_state_data = {
        'CurrentStage': 'Validator',
        'RequirementPointer': 'REQ-001',
        'is_protocol_update': False
    }

    def get_side_effect(key, default=None):
        return mock_state_data.get(key, default)

    def set_side_effect(key, value):
        mock_state_data[key] = value

    mock_state_instance.get.side_effect = get_side_effect
    mock_state_instance.set.side_effect = set_side_effect
    mock_state_instance.get_current_event_details.return_value = {"id": "REQ-001", "title": "Test Event"}

    # --- Patch external dependencies ---
    with patch('dw6.workflow.validator.ValidatorStage.validate', return_value=True):
        
        # --- Test Execution ---
        manager = WorkflowManager(mock_state_instance)
        manager.approve()

        # --- Assertions ---
        # Check that the stage was advanced correctly
        self.assertEqual(mock_state_data['CurrentStage'], 'Engineer')
        
        # Check that the correct state methods were called
        self.assertEqual(mock_state_instance.advance_requirement_pointer.call_count, 1)
        mock_state_instance.archive_completed_event.assert_not_called()
