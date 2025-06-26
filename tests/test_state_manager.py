import pytest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dw6.state_manager import WorkflowManager, WorkflowState

@pytest.fixture
def mock_state():
    """Fixture to create a mocked WorkflowState."""
    with patch('dw6.state_manager.WorkflowState') as MockState:
        instance = MockState.return_value
        instance.get.side_effect = lambda key, default=None: {
            "CurrentStage": "Deployer",
            "CycleCounter": "5"
        }.get(key, default)
        instance.data = {"CurrentStage": "Deployer", "CycleCounter": "5"}
        yield instance

@pytest.fixture
def manager(mock_state):
    """Fixture to create a WorkflowManager with a mocked state."""
    # Since the manager initializes its state in __init__, we need to patch before creating it
    return WorkflowManager()

def test_validate_deployment_success(manager):
    """Test that deployment validation succeeds when MCP calls are successful."""
    with patch('dw6.git_handler.mcp_push_files', return_value="some_commit_sha") as mock_push,
         patch('dw6.git_handler.mcp_create_and_push_tag') as mock_tag:
        
        result = manager._validate_deployment()

        assert result is True
        mock_push.assert_called_once_with("feat: Coder stage submission", ["src", "tests"])
        mock_tag.assert_called_once_with("v1.5", "some_commit_sha", "Release for cycle 5")

def test_validate_deployment_failure_and_exit(manager):
    """Test that deployment validation fails and exits if MCP push fails."""
    with patch('dw6.git_handler.mcp_push_files', return_value=None) as mock_push,
         patch('dw6.state_manager.WorkflowManager._increment_failure_counter') as mock_increment,
         patch('sys.exit') as mock_exit:

        result = manager._validate_deployment(allow_failures=False)

        assert result is False
        mock_push.assert_called_once()
        mock_increment.assert_called_once_with("mcp_push_files")
        mock_exit.assert_called_once_with(1)

def test_validate_deployment_failure_allowed(manager):
    """Test that deployment validation fails but continues if failures are allowed."""
    with patch('dw6.git_handler.mcp_push_files', return_value=None) as mock_push,
         patch('dw6.state_manager.WorkflowManager._increment_failure_counter') as mock_increment,
         patch('sys.exit') as mock_exit:

        result = manager._validate_deployment(allow_failures=True)

        assert result is False
        mock_push.assert_called_once()
        mock_increment.assert_called_once_with("mcp_push_files")
        mock_exit.assert_not_called()
