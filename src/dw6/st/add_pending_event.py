def add_pending_event(self, event, priority="Low"):
    """Adds a new event to the pending events queue according to its priority."""
    pending_events = self.get("PendingEvents", [])
    
    if priority == "High":
        pending_events.insert(0, event)
    elif priority == "Medium":
        mid_index = len(pending_events) // 2
        pending_events.insert(mid_index, event)
    else:  # Low priority
        pending_events.append(event)
        
    self.set("PendingEvents", pending_events)
    self.save()
