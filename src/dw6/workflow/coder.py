from ..git_handler import get_latest_commit_hash

class CoderStage:
    def __init__(self, state):
        self.state = state

    def validate(self, allow_failures=False):
        """
        Validates the Coder stage by ensuring a new commit has been made since the
        stage began.
        """
        start_commit_sha = self.state.get("CoderStartCommitSHA")
        if not start_commit_sha:
            print("--- Coder Validation Error: CoderStartCommitSHA not found in state.")
            print("--- This key should be set automatically when the workflow enters the Coder stage.")
            return False

        current_commit_sha = get_latest_commit_hash()

        if start_commit_sha == current_commit_sha:
            if allow_failures:
                print("--- Coder Validation Warning: No new commits found, but proceeding due to 'allow_failures' flag. ---")
                return True
            print("--- Coder Validation Failed: No new commits found. ---")
            print(f"--- The stage started at commit {start_commit_sha[:7]} and the current commit is the same. ---")
            print("--- Please commit your work before approving the Coder stage. ---")
            return False
        
        print("--- Coder Validation Passed: New commit detected. ---")
        print(f"--- Started at {start_commit_sha[:7]}, current is {current_commit_sha[:7]}. ---")
        return True
