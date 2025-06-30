import sys
from pathlib import Path

def advance_requirement_pointer(self):
    """
    Advances the RequirementPointer to the next available requirement file
    in the `events/` directory.

    This method scans the `events/` directory for all `REQ-*.json` files,
    sorts them alphanumerically, finds the current requirement, and then
    updates the pointer to the next one in the sequence.
    """
    events_dir = Path("events")
    if not events_dir.exists():
        print("--- Governor: CRITICAL: `events` directory not found. Cannot advance pointer. ---", file=sys.stderr)
        return False

    req_files = sorted([f for f in events_dir.glob("REQ-*.json")])
    if not req_files:
        print("--- Governor: No requirement files found in `events/`. Pointer remains unchanged. ---")
        return False

    current_id = self.state.get("RequirementPointer")
    if not current_id:
        next_id = req_files[0].stem
        self.state.set("RequirementPointer", next_id)
        print(f"--- Governor: Requirement pointer initialized to {next_id}. ---")
        return True

    current_path = events_dir / f"{current_id}.json"

    try:
        current_index = req_files.index(current_path)
        if current_index + 1 < len(req_files):
            next_id = req_files[current_index + 1].stem
            self.state.set("RequirementPointer", next_id)
            print(f"--- Governor: Requirement pointer advanced to {next_id}. ---")
            return True
        else:
            print("--- Governor: End of requirement queue reached. Pointer remains at the last requirement. ---")
            return False
    except ValueError:
        next_id = req_files[0].stem
        self.state.set("RequirementPointer", next_id)
        print(f"--- Governor: Could not find current requirement '{current_id}'. Resetting pointer to {next_id}. ---")
        return True
