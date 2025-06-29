from unittest.mock import patch, MagicMock, call
from dw6.state_manager import WorkflowManager
import json

def tvte(self):
    """
    Tests the transition from the Validator to the Engineer stage,
    simulating a filesystem-based requirement queue with correct patching
    and comparable mock file objects.
    """
    # --- Mock State ---
    mock_state_instance = self.mock_WorkflowState.return_value
    def get_side_effect(key, default=None):
        if key.startswith('failure_count'):
            return 0
        state = {
            'CurrentStage': 'Validator',
            'RequirementPointer': 'REQ-001'
        }
        return state.get(key, default)
    mock_state_instance.get.side_effect = get_side_effect

    # --- Mock Filesystem (with comparable mocks) ---
    mock_req1 = MagicMock(name='req1_file')
    mock_req1.stem = 'REQ-001'
    mock_req1.name = 'REQ-001.json'
    mock_req1.exists.return_value = True
    mock_req1.read_text.return_value = json.dumps({
        "id": "REQ-001", "title": "Test Event", "type": "Standard"
    })
    # Correct lambda that accepts self and other
    mock_req1.__lt__ = lambda self, other: self.name < other.name

    mock_req2 = MagicMock(name='req2_file')
    mock_req2.stem = 'REQ-002'
    mock_req2.name = 'REQ-002.json'
    # Correct lambda that accepts self and other
    mock_req2.__lt__ = lambda self, other: self.name < other.name

    mock_events_dir = MagicMock(name='events_dir')
    mock_events_dir.exists.return_value = True
    mock_events_dir.glob.return_value = [mock_req2, mock_req1] # Unsorted

    def truediv_side_effect(filename):
        if filename == 'REQ-001.json':
            return mock_req1
        return MagicMock()
    mock_events_dir.__truediv__.side_effect = truediv_side_effect

    def path_constructor_side_effect(path_str):
        if path_str == 'events':
            return mock_events_dir
        if path_str == 'events/REQ-001.json':
            return mock_req1
        return MagicMock(name=f'unhandled_path_{path_str}')

    # --- Test Execution ---
    patch_targets = [
        patch('dw6.workflow.kr.load_current_event_details.Path', side_effect=path_constructor_side_effect),
        patch('dw6.workflow.kr._advance_requirement_pointer.Path', side_effect=path_constructor_side_effect),
        patch('dw6.workflow.validator.ValidatorStage.validate', return_value=True)
    ]

    with patch_targets[0], patch_targets[1], patch_targets[2]:
        manager = WorkflowManager(mock_state_instance)
        manager.approve()

    # --- Assertions ---
    expected_calls = [
        call('RequirementPointer', 'REQ-002'),
        call('CurrentStage', 'Engineer')
    ]
    mock_state_instance.set.assert_has_calls(expected_calls, any_order=True)
