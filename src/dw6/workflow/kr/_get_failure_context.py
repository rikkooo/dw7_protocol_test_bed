def _get_failure_context(self):
    req_id = self.current_event.get("id", "unknown_req") if self.current_event else "unknown_req"
    failure_key = f"failure_count_{req_id}_{self.current_stage}"
    current_failure_count = self.state.get(failure_key, 0)
    return failure_key, current_failure_count
