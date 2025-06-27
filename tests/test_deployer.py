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

    @patch('git.Remote.push')
    @patch('dw6.git_handler.input', return_value='dummy_token_from_input')
    def test_credential_prompting(self, mock_input, mock_push, temp_project):
        """Tests that the user is prompted for credentials if not found."""
        # Remove the .env file to trigger the prompt
        (temp_project / ".env").unlink(missing_ok=True)

        state = WorkflowState()
        deployer = DeployerStage(state)

        # The git_handler.load_github_token will be called during the deployment process.
        # We patch the actual git push command to avoid network calls.
        deployer._execute_standard_deployment()

        # Check that the user was prompted and the token was saved
        mock_input.assert_called_once()
        env_file = temp_project / ".env"
        assert env_file.exists()
        assert "GITHUB_TOKEN=\"dummy_token_from_input\"" in env_file.read_text()
