import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from dw6.workflow.deployer import DeployerStage

@pytest.fixture
def temp_project_for_docs(tmp_path):
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / "docs").mkdir()
    (project_dir / "docs" / "reqs").mkdir()
    return project_dir

class TestFinalDocumentation:

    @patch('dw6.workflow.deployer.DeployerStage._generate_final_readme')
    def test_readme_generation_on_project_completion(self, mock_generate_readme, temp_project_for_docs, monkeypatch):
        """Tests that the final README is generated when all requirements are deployed."""
        monkeypatch.chdir(temp_project_for_docs)
        
        # Create a requirements file with all items deployed
        req_file = temp_project_for_docs / "docs" / "PROJECT_REQUIREMENTS.md"
        req_file.write_text("[D] [C] REQ-001\n[D] [H] REQ-002")

        # Mock the state and config
        mock_state = MagicMock()
        deployer = DeployerStage(state=mock_state)
        deployer.validate()

        mock_generate_readme.assert_called_once()

    @patch('dw6.workflow.deployer.DeployerStage._generate_final_readme')
    @patch('dw6.workflow.deployer.DeployerStage._execute_standard_deployment')
    def test_no_readme_generation_if_project_incomplete(self, mock_standard_deployment, mock_generate_readme, temp_project_for_docs, monkeypatch):
        """Tests that the final README is NOT generated if requirements are pending."""
        monkeypatch.chdir(temp_project_for_docs)
        
        # Create a requirements file with a pending item
        req_file = temp_project_for_docs / "docs" / "PROJECT_REQUIREMENTS.md"
        req_file.write_text("[D] [C] REQ-001\n[P] [H] REQ-002")

        # Mock the state and config, and git_handler to avoid errors
        mock_state = MagicMock()
        with patch('dw6.git_handler.check_for_workflow_changes', return_value=False), patch.object(DeployerStage, '_load_config', return_value={'PROJECT_REPO_URL': 'dummy'}):
            deployer = DeployerStage(state=mock_state)
            deployer.validate()

        mock_generate_readme.assert_not_called()
        mock_standard_deployment.assert_called_once()
