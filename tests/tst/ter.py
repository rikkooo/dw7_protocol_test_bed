from unittest.mock import patch
from dw6.state_manager import WorkflowManager

# Note: The original test was named test_engineer_to_researcher_transition
def ter(self):
    """
    Tests the transition from the Engineer to the Researcher stage.
    """
    mock_state_instance = self.mock_WorkflowState.return_value
    mock_state_instance.get.return_value = 'Engineer'
    manager = WorkflowManager(mock_state_instance)

    with patch('dw6.workflow.engineer.EngineerStage.validate', return_value=True):
        manager.approve(needs_research=True)

    mock_state_instance.set.assert_called_with('CurrentStage', 'Researcher')
