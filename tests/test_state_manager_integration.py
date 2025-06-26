import pytest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dw6.state_manager import WorkflowManager

@pytest.fixture
def manager_fixture():
    """Provides a WorkflowManager instance with a clean state for each test."""
    # Use mock_open to simulate the state file
    m = mock_open()
    with patch('builtins.open', m):
        # Ensure the logs directory exists for the state file
        Path("logs").mkdir(exist_ok=True)
        # Create a manager, which will initialize a fresh state
        manager = WorkflowManager()
        # Reset to a known stage for testing
        manager.set_stage("Deployer")
        yield manager

def test_failure_counter_increments_on_failure(manager_fixture):
    """Integration test to ensure failure counter is incremented on deployment failure."""
    manager = manager_fixture
    
    # Check initial state (should be no failure counter)
    assert manager.state.get("FailureCounters.Deployer.mcp_push_files") is None

    # Simulate a failed deployment push
    with patch('dw6.git_handler.mcp_push_files', return_value=None),
         patch('sys.exit'): # Patch sys.exit to prevent test termination
        manager._validate_deployment(allow_failures=False)

    # Check that the counter was incremented
    assert manager.state.get("FailureCounters.Deployer.mcp_push_files") == "1"

    # Simulate another failure
    with patch('dw6.git_handler.mcp_push_files', return_value=None),
         patch('sys.exit'): 
        manager._validate_deployment(allow_failures=False)

    # Check that the counter is now 2
    assert manager.state.get("FailureCounters.Deployer.mcp_push_files") == "2"

def test_failure_counter_resets_on_stage_advancement(manager_fixture):
    """Integration test to ensure failure counters are reset when a stage is advanced."""
    manager = manager_fixture

    # First, create a failure counter in the 'Deployer' stage
    with patch('dw6.git_handler.mcp_push_files', return_value=None),
         patch('sys.exit'):
        manager._validate_deployment(allow_failures=False)
    
    assert manager.state.get("FailureCounters.Deployer.mcp_push_files") == "1"

    # Now, successfully validate and advance the stage
    # This will move from 'Deployer' to 'Finished'
    with patch('dw6.git_handler.mcp_push_files', return_value="sha123"),\
         patch('dw6.git_handler.mcp_create_and_push_tag'):
        manager.approve() # This calls _validate_deployment -> _advance_stage

    # The stage should now be 'Finished'
    assert manager.current_stage == "Finished"

    # Now, let's imagine we start a new cycle and go back to 'Deployer'
    # The _reset_failure_counters should have been called for 'Deployer' upon leaving it.
    # To test this, we can manually check the state data because advancing to 'Finished'
    # doesn't automatically loop back. The logic in _advance_stage calls reset on the *next* stage.
    # Let's manually set the stage back to Deployer and check.
    
    # The core check: was the key deleted from the state data?
    # We need to inspect the state data directly before it gets re-saved.
    # The reset happens upon advancing TO the next stage, so we check the state for the OLD stage.
    # Let's re-run the logic slightly differently to make the test clearer.

    # 1. Set stage to Validator
    manager.set_stage("Validator")
    # 2. Create a failure counter for Validator
    manager.state.set("FailureCounters.Validator.some_check", "3")
    manager.state.save()
    assert manager.state.get("FailureCounters.Validator.some_check") == "3"

    # 3. Advance from Validator to Deployer
    with patch.object(manager, '_validate_validator', return_value=True):
         manager.approve()

    # 4. Check that the counter for the *new* stage (Deployer) was reset.
    # In this case, we are checking that if any counters *had* existed for Deployer, they'd be gone.
    # A better test is to check that the counter for the *previous* stage is still there,
    # and the one for the *new* stage is not.
    # The current implementation resets the counters for the STAGE YOU ARE ENTERING.
    assert "FailureCounters.Deployer.mcp_push_files" not in manager.state.data
    assert manager.state.get("FailureCounters.Validator.some_check") == "3" # The old one should persist
