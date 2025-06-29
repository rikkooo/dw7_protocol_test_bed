from unittest.mock import patch
from dw6.state_manager import WorkflowManager

# Note: The original test was named test_researcher_to_coder_transition
def trc(self):
    """
    Tests the transition from the Researcher to the Coder stage.
    """
    mock_state_instance = self.mock_WorkflowState.return_value

    def get_side_effect(key, default=None):
        state = {
            'CurrentStage': 'Researcher',
            'is_protocol_update': False
        }
        return state.get(key, default)

    mock_state_instance.get.side_effect = get_side_effect

    manager = WorkflowManager(mock_state_instance)

    with patch('dw6.workflow.researcher.ResearcherStage.validate', return_value=True):
        manager.approve()

    mock_state_instance.set.assert_called_with('CurrentStage', 'Coder')
