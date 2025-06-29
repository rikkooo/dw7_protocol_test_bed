import re
import sys
import traceback

def _create_red_flag_requirement(self, exception):
    """
    Creates a special 'Red Flag' requirement when a critical failure threshold is met.
    This requirement is prioritized to force a manual, intelligent review of the failure.
    """
    try:
        # Determine the next requirement ID
        all_ids = []
        pending_events = self.state.get("PendingEvents", [])
        processed_events = self.state.get("ProcessedEvents", [])
        for event in pending_events + processed_events:
            if (num := re.search(r'REQ-DW8-(\d+)', event.get('id', ''))):
                all_ids.append(int(num.group(1)))

        next_id = max(all_ids) + 1 if all_ids else 1
        new_req_id = f"REQ-DW8-{next_id:03d}"

        # Create the detailed red flag requirement file
        red_flag_path = f"docs/reqs/{new_req_id}.md"
        exc_type = type(exception).__name__
        exc_message = str(exception).replace('\n', '\n    ')
        tb_str = "".join(traceback.format_tb(exception.__traceback__)).replace('\n', '\n      ')

        red_flag_content = f"""### ID: {new_req_id}\n\n- **Title:** Red Flag: Unhandled Critical Failure in {self.current_stage} Stage\n- **Status:** `Pending`\n- **Priority:** `Critical`\n- **Details:** The workflow encountered a critical failure after multiple retries. The system has been reset to the Engineer stage to re-evaluate the approach.\n- **SMRs:**\n  - [ ] Analyze the failure context below to understand the root cause.\n  - [ ] Formulate a new plan to address the failure.\n  - [ ] Implement the new plan.\n- **Failure Context:**\n  - **Exception Type:** `{exc_type}`\n  - **Exception Message:**\n    ```\n    {exc_message}\n    ```\n  - **Traceback:**\n    ```\n    {tb_str}\n    ```\n"""
        with open(red_flag_path, "w") as f:
            f.write(red_flag_content)
        print(f"Successfully created red flag file: {red_flag_path}")

        # Create the new event object
        new_event = {
            "id": new_req_id,
            "title": f"Red Flag: Unhandled Critical Failure in {self.current_stage} Stage",
            "status": "Pending",
            "priority": "Critical",
            "path": f"./reqs/{new_req_id}.md"
        }

        # Prepend the new event to the pending queue to give it top priority
        self.state.add_pending_event(new_event, priority="High")

        print(f"Successfully injected {new_req_id} into the pending events queue.")

        return new_req_id

    except Exception as e:
        print(f"FATAL: Could not create Red Flag requirement. Error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return None
