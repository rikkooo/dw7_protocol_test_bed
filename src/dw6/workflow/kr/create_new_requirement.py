import json
import re

def create_new_requirement(self, requirement_id, title, description, acceptance_criteria, event_type="Standard", priority="Normal"):
    """
    Creates a new requirement JSON file and adds a corresponding event to the pending queue.
    """
    event_file_path = f"events/{requirement_id}.json"
    event_data = {
        "id": requirement_id,
        "title": title,
        "description": description,
        "acceptance_criteria": acceptance_criteria,
        "type": event_type,
        "priority": priority,
        "status": "Pending"
    }

    with open(event_file_path, "w") as f:
        json.dump(event_data, f, indent=2)
    print(f"Successfully created requirement file: {event_file_path}")

    # The event added to the pending queue is just a summary
    new_event = {
        "id": requirement_id,
        "title": title,
        "priority": priority
    }

    self.state.add_pending_event(new_event, priority=priority)
    print(f"Successfully injected {requirement_id} into the pending events queue.")

    return requirement_id
