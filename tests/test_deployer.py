import pytest
import os
import git
from pathlib import Path
from unittest.mock import patch, MagicMock

from dw6.workflow.deployer import DeployerStage
from dw6.state_manager import WorkflowState


class TestDeployerStage:

    @pytest.fixture
    def temp_project(self, tmp_path):
        # Create a temporary project directory
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()

        # Initialize a git repository
        repo = git.Repo.init(project_dir)

        # Create a dummy file and commit it
        (project_dir / "README.md").write_text("Initial commit")
        repo.git.add(".")
        repo.index.commit("Initial commit")

        # Add a dummy tag for versioning
        repo.create_tag("v7.0.0", message="Initial version")

        # Create a deployer config file
        docs_dir = project_dir / "docs"
        docs_dir.mkdir()
        (docs_dir / "DEPLOYER_CONFIGURATION.md").write_text(
            "PROJECT_REPO_URL: https://github.com/user/test-project.git\n"
            "OFFICIAL_PROTOCOL_DIRECTORY: /tmp/dw_official\n"
            "OFFICIAL_PROTOCOL_REPOSITORY: https://github.com/windsurf/dw-protocol.git\n"
        )

        # Create a dummy .env file
        (project_dir / ".env").write_text("GITHUB_TOKEN=dummy_token_from_file")

        # Create a pyproject.toml to make it a valid project
        (project_dir / "pyproject.toml").write_text(
            """[project]
name = "test-project"
version = "0.1.0"
"""
        )

        # Change the current working directory to the project directory
        os.chdir(project_dir)

        yield project_dir

    def test_config_loading(self, temp_project):
        """Tests that the deployer stage correctly loads configuration."""
        state = WorkflowState()
        deployer = DeployerStage(state)

        assert deployer.config["PROJECT_REPO_URL"] == "https://github.com/user/test-project.git"
        assert deployer.config["OFFICIAL_PROTOCOL_DIRECTORY"] == "/tmp/dw_official"

    @patch('git.remote.Remote.push')
    @patch('dw6.git_handler.input', return_value='dummy_token_from_input')
    @patch('dw6.git_handler.save_github_token')
    def test_credential_prompting_on_push_failure(self, mock_save_token, mock_input, mock_push, temp_project):
        """Tests that the user is prompted for credentials if the git push fails with an auth error."""
        # Arrange
        # Ensure no environment token is present
        os.environ.pop('GITHUB_TOKEN', None)
        # Start with a bad token in the .env to force the initial failure
        (temp_project / ".env").write_text('GITHUB_TOKEN="bad_token"')
    
        repo = git.Repo(temp_project)
        repo.create_remote('origin', 'https://github.com/dummy/dummy.git')
    
        # Configure the mock for Remote.push
        # Simulate an authentication failure on the first call, and success on the second
        mock_push.side_effect = [
            git.exc.GitCommandError('push', 128, stderr='fatal: Authentication failed'),
            None  # Success
        ]
    
        # Act
        from dw6.git_handler import push_to_remote
        # Call the function without tags, just a standard push
        push_to_remote(repo=repo)
    
        # Assert
        # The push should have been attempted twice
        assert mock_push.call_count == 2
        # The user should have been prompted for a new token
        mock_input.assert_called_once()
        # The new token should have been saved
        mock_save_token.assert_called_once_with('dummy_token_from_input', temp_project / '.env')

    @patch('dw6.git_handler.git.Repo')
    @patch('dw6.workflow.dp.exec_proto_evo.git_handler')
    def test_protocol_evolution_dual_push(self, mock_git_handler, mock_repo, temp_project):
        """Tests that protocol evolution triggers a push to both project and official repos."""
        # Setup state for protocol evolution
        state = WorkflowState()
        state.set("is_protocol_update", "true")
        deployer = DeployerStage(state)

        # Mock the git repo and remotes
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.active_branch.name = 'main' # Mock active branch

        mock_official = MagicMock()
        mock_official.name = 'official_protocol_repo'
        mock_repo_instance.create_remote.return_value = mock_official

        # Execute the validation, which should trigger protocol evolution
        deployer.validate()

        # Assert that the project repo push was called via the handler
        mock_git_handler.push_to_remote.assert_called_once_with(
            files=['.'], 
            message='Pushing protocol update to project repository', 
            repo=mock_repo_instance
        )

        # Assert that the official repo push was called on the remote object
        mock_official.push.assert_called_once()
