def _advance_requirement_pointer(self):
    if not self.pending_events:
        print("--- Governor: No pending events. Pointer remains unchanged. ---")
        return

    current_id = self.state.get("RequirementPointer")
    try:
        current_index = next(i for i, event in enumerate(self.pending_events) if event.get("id") == current_id)
        next_index = (current_index + 1) % len(self.pending_events)
        next_id = self.pending_events[next_index].get("id")
        self.state.set("RequirementPointer", next_id)
        print(f"--- Governor: Requirement pointer advanced to {next_id}. ---")
    except (StopIteration, IndexError):
        # If current ID not found or list is empty, point to the first event
        if self.pending_events:
            next_id = self.pending_events[0].get("id")
            self.state.set("RequirementPointer", next_id)
            print(f"--- Governor: Could not find current requirement. Resetting pointer to {next_id}. ---")
