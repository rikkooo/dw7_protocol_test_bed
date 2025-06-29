import subprocess
import sys

class ValidatorStage:
    def __init__(self, state):
        self.state = state

    def validate(self, allow_failures=False):
        """
        Runs tests using `uv run pytest` to ensure execution within the
        correct virtual environment.
        """
        try:
            print("--- Governor: Running pytest validation... ---")
            # REQ-DW8-018: Use `uv run` to ensure correct environment
            result = subprocess.run(
                ["uv", "run", "pytest"],
                check=True,
                capture_output=True,
                text=True
            )
            print("--- Governor: Pytest validation successful. ---")
            self.state.reset_failure_counter("Validator", "pytest")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during test validation: {e}", file=sys.stderr)
            print(e.stderr, file=sys.stderr)
            self.state.increment_failure_counter("Validator", "pytest")
            if allow_failures:
                print("--- Governor: Test failures ignored as per request. ---")
                return True
            return False
