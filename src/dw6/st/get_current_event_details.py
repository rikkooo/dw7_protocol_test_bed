import json
import sys
from pathlib import Path

def get_current_event_details(self):
    """
    Loads the full details of the current requirement from its JSON file.
    """
    current_id = self.get("RequirementPointer")
    if not current_id:
        print("--- Governor: CRITICAL: No RequirementPointer set. Cannot load event details. ---", file=sys.stderr)
        return None

    event_path = Path(f"events/{current_id}.json")
    if not event_path.exists():
        print(f"--- Governor: CRITICAL: Requirement file not found for {current_id} at {event_path}. ---", file=sys.stderr)
        return None

    try:
        with open(event_path, 'r') as f:
            event_details = json.load(f)
        return event_details
    except (json.JSONDecodeError, IOError) as e:
        print(f"--- Governor: CRITICAL: Failed to read or parse requirement file {event_path}. Error: {e} ---", file=sys.stderr)
        return None
