import sys

def load_current_event_details(self):
    """
    Finds the current event summary from the pending queue based on the
    RequirementPointer and triggers the loading of its full details.
    """
    req_pointer = self.state.get("RequirementPointer")
    if not req_pointer:
        print("--- Governor: No requirement pointer found. Cannot load event. ---", file=sys.stderr)
        self.current_event = None
        return

    try:
        current_event_summary = next((event for event in self.pending_events if event.get("id") == req_pointer), None)

        if current_event_summary:
            # Delegate to the details loader, which is responsible for setting self.current_event
            self._load_event_details(current_event_summary)
        else:
            print(f"--- Governor: Could not find event with ID {req_pointer} in the pending queue. ---", file=sys.stderr)
            self.current_event = None
    except Exception as e:
        print(f"--- Governor: An unexpected error occurred while loading pending events: {e} ---", file=sys.stderr)
        self.current_event = None
