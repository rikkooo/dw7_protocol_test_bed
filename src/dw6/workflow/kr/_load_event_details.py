import json
import sys
from pathlib import Path

def _load_event_details(self, event_summary):
    """
    Loads the full details of an event from its JSON file, constructing
    the self.current_event object.
    """
    event_id = event_summary.get("id")
    # Correct path to look inside events/ for .json files
    event_file = Path("events") / f"{event_id}.json"

    if event_file.exists():
        try:
            with open(event_file, "r") as f:
                event_data = json.load(f)

            # Construct the current_event object from the JSON data.
            # The status is set to 'In Progress' because loading it means we are working on it.
            self.current_event = {
                "id": event_data.get("id", event_id),
                "title": event_data.get("title", "Title not found"),
                "description": event_data.get("description", "Description not found"),
                "acceptance_criteria": event_data.get("acceptance_criteria", []),
                "type": event_data.get("type", "Standard"),
                "status": "In Progress",
                "details": event_data
            }

        except (json.JSONDecodeError, Exception) as e:
            print(f"--- Governor: ERROR parsing event file {event_file}: {e} ---", file=sys.stderr)
            self.current_event = {"id": event_id, "title": f"Details not found (parsing error for {event_id})"}
    else:
        print(f"--- Governor: WARNING: Event file not found at {event_file} for {event_id} ---", file=sys.stderr)
        self.current_event = {"id": event_id, "title": f"Details not found (file missing for {event_id})"}
