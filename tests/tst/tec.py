from unittest.mock import patch
from dw6.state_manager import WorkflowManager

# Note: The original test was named test_engineer_to_coder_transition
def tec(self):
    """
    Tests the transition from the Engineer to the Coder stage.
    """
    mock_state_instance = self.mock_WorkflowState.return_value

    def get_side_effect(key, default=None):
        if key == 'CurrentStage':
            return 'Engineer'
        if key == 'RequirementPointer':
            return 'REQ-001'
        # The advance_stage logic needs PendingEvents and the current event
        if key == 'PendingEvents':
            return [{'id': 'REQ-001', 'type': 'Standard'}]
        return default
    mock_state_instance.get.side_effect = get_side_effect
    
    manager = WorkflowManager(mock_state_instance)
    # The advance_stage logic also checks the type of the current event
    manager.kernel.current_event = {"type": "Standard"}

    with patch('dw6.workflow.engineer.EngineerStage.validate', return_value=True):
        manager.approve()

    mock_state_instance.set.assert_called_with('CurrentStage', 'Coder')
