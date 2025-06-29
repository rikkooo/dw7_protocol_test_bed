def _reset_failure_counters(self, stage):
    req_id = self.current_event.get("id", "unknown_req") if self.current_event else "unknown_req"
    failure_key = f"failure_count_{req_id}_{stage}"
    self.state.set(failure_key, 0)
