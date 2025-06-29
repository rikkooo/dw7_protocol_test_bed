from dw6.workflow.engineer import EngineerStage
from dw6.workflow.researcher import ResearcherStage
from dw6.workflow.coder import CoderStage
from dw6.workflow.validator import ValidatorStage
from dw6.workflow.deployer import DeployerStage
from dw6.workflow.rehearsal import RehearsalStage

def _load_stage_module(self):
    stage_classes = {
        "Engineer": EngineerStage,
        "Researcher": ResearcherStage,
        "Coder": CoderStage,
        "Validator": ValidatorStage,
        "Deployer": DeployerStage,
        "Rehearsal": RehearsalStage,
    }
    stage_class = stage_classes.get(self.current_stage_name)
    if not stage_class:
        raise ValueError(f"Unknown stage: {self.current_stage_name}")
    return stage_class(self.state)
