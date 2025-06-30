from unittest.mock import patch, MagicMock
from dw6.state_manager import WorkflowManager

# Note: The original test was named test_engineer_to_researcher_transition
def ter(self):
    """
    Tests the transition from the Engineer to the Researcher stage when needs_research is True.
    """
    mock_state_instance = self.mock_WorkflowState.return_value
    
    def get_side_effect(key, default=None):
        state = {
            'CurrentStage': 'Engineer',
            'is_protocol_update': False,
            'RequirementPointer': 'REQ-001'
        }
        return state.get(key, default)

    mock_state_instance.get.side_effect = get_side_effect
    
    manager = WorkflowManager(mock_state_instance)
    # We mock the method on the manager instance directly to prevent file system access
    manager.get_current_event_details = MagicMock(return_value={"id": "REQ-001", "type": "Sherlock"})

    with patch('dw6.workflow.engineer.EngineerStage.validate', return_value=True):
        manager.approve(needs_research=True)

    mock_state_instance.set.assert_called_with('CurrentStage', 'Researcher')
