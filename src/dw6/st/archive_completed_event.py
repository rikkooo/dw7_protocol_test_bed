def archive_completed_event(self, event_to_archive):
    """
    Moves a completed event to the ProcessedEvents list.
    This method assumes the event is the currently active one, not one from the pending queue.
    """
    if not event_to_archive or 'id' not in event_to_archive:
        return

    event_id_to_archive = event_to_archive['id']
    processed_events = self.data.get('ProcessedEvents', [])

    # Simply add the completed event to the processed list.
    # The advancement of the requirement pointer is handled by a separate method.
    processed_events.insert(0, event_to_archive)
    self.data['ProcessedEvents'] = processed_events
    print(f"--- Governor: Event '{event_id_to_archive}' archived. ---")

    self.save()
