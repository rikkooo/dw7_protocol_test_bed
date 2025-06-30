def archive_completed_event(self, event):
    """Moves a completed event from the pending queue to the processed queue."""
    pending_events = self.state.get("PendingEvents", [])
    processed_events = self.state.get("ProcessedEvents", [])

    # Remove from pending
    pending_events = [e for e in pending_events if e.get('id') != event.get('id')]
    self.state.set("PendingEvents", pending_events)

    # Add to processed
    processed_events.append(event)
    self.state.set("ProcessedEvents", processed_events)
    self.state.save()
