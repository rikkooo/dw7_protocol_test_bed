import sys
import importlib
sys.path.insert(0, '/home/ubuntu/devs/dw7_protocol_test_bed/src')

# Force reload of the git_handler module to bypass import cache
import dw6.git_handler
importlib.reload(dw6.git_handler)

from dw6.workflow.deployer import DeployerStage

class MockState:
    def get(self, key):
        return None
    def set(self, key, value):
        pass

print("--- Governor: Forcing module reload and triggering final documentation generation. ---")
state = MockState()
deployer = DeployerStage(state)
success = deployer.validate()

if success:
    print("--- Governor: Project completion process finished successfully. ---")
else:
    print("--- Governor: Project completion process failed. ---", file=sys.stderr)
