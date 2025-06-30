from unittest.mock import patch, MagicMock
from dw6.state_manager import WorkflowManager

# Note: The original test was named test_engineer_to_coder_transition
def tec(self):
    """
    Tests the transition from the Engineer to the Coder stage for an 'Execution' type requirement.
    """
    mock_state_instance = self.mock_WorkflowState.return_value

    def get_side_effect(key, default=None):
        if key == 'CurrentStage':
            return 'Engineer'
        # The RequirementPointer is needed by the kernel to get event details
        if key == 'RequirementPointer':
            return 'REQ-001'
        return default
    mock_state_instance.get.side_effect = get_side_effect
    
    manager = WorkflowManager(mock_state_instance)
    # We mock the method on the manager instance directly to prevent file system access
    manager.get_current_event_details = MagicMock(return_value={"id": "REQ-001", "type": "Execution"})

    with patch('dw6.workflow.engineer.EngineerStage.validate', return_value=True):
        manager.approve()

    mock_state_instance.set.assert_called_with('CurrentStage', 'Coder')
