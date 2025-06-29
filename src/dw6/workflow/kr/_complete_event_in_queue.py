import sys

def _complete_event_in_queue(self):
    """
    Moves the current event from the pending queue to the processed queue.
    """
    current_id = self.state.get("RequirementPointer")
    event_to_move = next((event for event in self.pending_events if event.get("id") == current_id), None)

    if not event_to_move:
        print(f"--- Governor: Could not find event {current_id} to complete. ---", file=sys.stderr)
        return

    self.state.archive_completed_event(event_to_move)
    print(f"--- Governor: Event {current_id} completed and archived. ---")
