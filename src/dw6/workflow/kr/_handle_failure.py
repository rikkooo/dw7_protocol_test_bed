import sys

FAILURE_THRESHOLD = 3

def _handle_failure(self, exception):
    failure_key, current_failure_count = self._get_failure_context()
    self.state.increment(failure_key)
    
    # Ensure current_failure_count is an integer before comparison
    current_failure_count = int(current_failure_count)

    if current_failure_count + 1 >= FAILURE_THRESHOLD:
        print(f"--- Governor: CRITICAL FAILURE THRESHOLD REACHED for stage {self.current_stage}. ---", file=sys.stderr)
        self._enter_rehearsal_stage(exception)
    else:
        print(f"--- Governor: Failure count for stage {self.current_stage} is now {current_failure_count + 1}. Retrying... ---", file=sys.stderr)
