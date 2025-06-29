from unittest.mock import patch
from dw6.state_manager import WorkflowManager

# Note: The original test was part of test_validator_stage_transitions
def tvte(self):
    """
    Tests the transition from the Validator to the Engineer stage.
    """
    mock_state_instance = self.mock_WorkflowState.return_value
    def get_side_effect(key, default=None):
        if key == 'CurrentStage':
            return 'Validator'
        if key == 'RequirementPointer':
            return 'REQ-001'
        if key == 'PendingEvents':
            return [{'id': 'REQ-001', 'title': 'Test Event'}]
        if key.startswith('failure_count'):
            return 0
        return default
    mock_state_instance.get.side_effect = get_side_effect
    manager = WorkflowManager(mock_state_instance)

    # Mock the event type for a standard event
    manager.kernel.current_event = {"type": "Standard"}

    with patch('dw6.workflow.validator.ValidatorStage.validate', return_value=True):
        manager.approve()

    mock_state_instance.set.assert_called_with('CurrentStage', 'Engineer')
