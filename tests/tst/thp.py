from unittest.mock import patch, mock_open
from dw6.state_manager import WorkflowManager

# Note: The original test was named test_high_priority_event_insertion
def thp(self):
    """
    Tests the insertion of a high-priority event into the pending queue.
    """
    mock_state_instance = self.mock_WorkflowState.return_value
    mock_state_instance.get.return_value = 'Engineer'  # Mock stage to allow manager initialization
    manager = WorkflowManager(mock_state_instance)

    # The create_new_requirement method opens a file to write the new event, so we mock open
    m = mock_open()
    with patch('builtins.open', m):
        manager.create_new_requirement(
            'REQ-002',
            'High Priority Task',
            'This should be first.',
            ['Criterion 1'],
            priority='High'
        )

    # Verify that the state manager's `add_pending_event` method was called with the correct event summary and priority
    expected_event = {
        "id": "REQ-002",
        "title": "High Priority Task",
        "priority": "High"
    }
    mock_state_instance.add_pending_event.assert_called_once_with(expected_event, priority='High')
