import json
import sys
from pathlib import Path

def load_current_event_details(self):
    """
    Loads the active requirement directly from its JSON file in the `events/`
    directory, based on the `RequirementPointer` in the workflow state.

    This method represents the modernized, event-driven protocol, where the
    filesystem is the source of truth for requirement definitions.
    """
    req_pointer = self.state.get("RequirementPointer")
    if not req_pointer:
        print("--- Governor: No requirement pointer found. Cannot load event. ---", file=sys.stderr)
        self.current_event = None
        return

    event_file_path = Path(f"events/{req_pointer}.json")

    if not event_file_path.exists():
        print(f"--- Governor: CRITICAL: Requirement file not found for {req_pointer} at {event_file_path}. ---", file=sys.stderr)
        self.current_event = None
        return

    try:
        with open(event_file_path, 'r') as f:
            self.current_event = json.load(f)
    except json.JSONDecodeError as e:
        print(f"--- Governor: CRITICAL: Failed to decode JSON from {event_file_path}. Error: {e} ---", file=sys.stderr)
        self.current_event = None
    except Exception as e:
        print(f"--- Governor: An unexpected error occurred while loading {event_file_path}: {e} ---", file=sys.stderr)
        self.current_event = None
