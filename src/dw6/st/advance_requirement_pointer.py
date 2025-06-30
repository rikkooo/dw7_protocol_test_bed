def advance_requirement_pointer(self):
    """
    Advances the RequirementPointer to the next event in the PendingEvents queue.
    If the queue is empty, the pointer is set to None.
    """
    pending_events = self.data.get('PendingEvents', [])

    if pending_events:
        # Get the next event from the top of the queue
        next_event = pending_events.pop(0)
        next_event_id = next_event.get('id')
        self.data['RequirementPointer'] = next_event_id
        self.data['PendingEvents'] = pending_events
        print(f"--- Governor: Requirement pointer advanced to '{next_event_id}'. ---")
    else:
        self.data['RequirementPointer'] = None
        print("--- Governor: Pending events queue is empty. Requirement pointer set to None. ---")

    self.save()
