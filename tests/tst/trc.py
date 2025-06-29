from unittest.mock import patch
from dw6.state_manager import WorkflowManager

# Note: The original test was named test_researcher_to_coder_transition
def trc(self):
    """
    Tests the transition from the Researcher to the Coder stage.
    """
    mock_state_instance = self.mock_WorkflowState.return_value
    mock_state_instance.get.return_value = 'Researcher'
    manager = WorkflowManager(mock_state_instance)

    with patch('dw6.workflow.researcher.ResearcherStage.validate', return_value=True):
        manager.approve()

    mock_state_instance.set.assert_called_with('CurrentStage', 'Coder')
