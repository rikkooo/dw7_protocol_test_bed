from unittest.mock import patch
from dw6.state_manager import WorkflowManager

# Note: The original test was named test_failure_counter_and_rehearsal_transition
def tfc(self):
    """
    Tests the failure counter logic and the transition to the Rehearsal stage.
    """
    mock_state_instance = self.mock_WorkflowState.return_value

    def get_side_effect_for_tfc(key, default=None):
        # This is the dynamic key the kernel uses to get the failure count.
        if key == 'failure_count_REQ-001_Validator':
            # The test cases will overwrite this mock's return_value as needed.
            return mock_state_instance.get_failure_counter.return_value
        if key == 'CurrentStage':
            return 'Validator'
        if key == 'RequirementPointer':
            return 'REQ-001'
        if key == 'PendingEvents':
            return [{'id': 'REQ-001', 'title': 'Test Event'}]
        return default
    mock_state_instance.get.side_effect = get_side_effect_for_tfc

    manager = WorkflowManager(mock_state_instance)
    manager.kernel.current_event = {"id": "REQ-001"}

    # Patch the validate method to simulate a failure
    with patch('dw6.workflow.validator.ValidatorStage.validate', return_value=False):
        # --- Test Case 1: Failure count BELOW threshold ---
        with patch.object(manager.kernel, '_handle_failure') as mock_handle_failure, \
             patch.object(manager.kernel, 'advance_stage') as mock_advance_stage:

            mock_state_instance.get_failure_counter.return_value = 2
            manager.approve()

            # Check that the failure was handled and the stage was not advanced
            mock_handle_failure.assert_called_once()
            mock_advance_stage.assert_not_called()

        # --- Reset mocks for the next test case ---
        mock_state_instance.set.reset_mock()

        # --- Test Case 2: Failure count AT threshold ---
        # Let the REAL _handle_failure method run to test the transition
        mock_state_instance.get_failure_counter.return_value = 3
        manager.approve()

        # Check that we transitioned to the Rehearsal stage
        mock_state_instance.set.assert_any_call('CurrentStage', 'Rehearsal')
