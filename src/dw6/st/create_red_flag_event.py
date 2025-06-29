import json
import re
import sys
import traceback
from pathlib import Path

def create_red_flag_event(self, exception, stage):
    """
    Creates a special 'Red Flag' requirement JSON file when a critical failure occurs.
    """
    try:
        events_dir = Path("events")
        events_dir.mkdir(exist_ok=True)
        
        existing_files = list(events_dir.glob("REQ-DW8-OS-*.json"))
        all_ids = [int(re.search(r'(\d+)', f.stem).group(1)) for f in existing_files if re.search(r'(\d+)', f.stem)]
        
        next_id_num = max(all_ids) + 1 if all_ids else 1
        new_req_id = f"REQ-DW8-OS-{next_id_num:03d}"

        exc_type = type(exception).__name__
        exc_message = str(exception)
        tb_str = "".join(traceback.format_tb(exception.__traceback__))

        red_flag_event = {
            "id": new_req_id,
            "title": f"Red Flag: Unhandled Critical Failure in {stage} Stage",
            "description": f"The workflow encountered a critical, unrecoverable error.\n\n**Exception Type:** {exc_type}\n**Message:** {exc_message}\n\n**Traceback:**\n```\n{tb_str}```",
            "acceptance_criteria": [
                {"text": "Analyze the traceback and identify the root cause.", "completed": False},
                {"text": "Implement a fix for the underlying issue.", "completed": False},
                {"text": "Add a new test case that reproduces the failure to prevent regressions.", "completed": False}
            ],
            "status": "Pending",
            "priority": "Critical",
            "type": "Execution"
        }

        event_path = events_dir / f"{new_req_id}.json"
        with open(event_path, 'w') as f:
            json.dump(red_flag_event, f, indent=2)

        self.add_pending_event(red_flag_event)
        print(f"--- Governor: Created critical red flag event {new_req_id} at {event_path}. ---")
        return new_req_id
    except Exception as e:
        print(f"--- Governor: CRITICAL: Failed to create red flag event. Error: {e} ---", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return None
