import subprocess
import sys

class ValidatorStage:
    def __init__(self, state):
        self.state = state

    def validate(self, allow_failures=False):
        """
        Runs tests using pytest, saves the Python executable path to the state,
        and returns True on success or if failures are allowed.
        """
        # Discover the Python executable from the current environment
        python_executable = sys.executable
        self.state.set("PythonExecutablePath", python_executable)
        print(f"--- Governor: Python executable path set to {python_executable} ---")

        try:
            print("--- Governor: Running pytest validation... ---")
            result = subprocess.run(
                [python_executable, "-m", "pytest"], 
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
