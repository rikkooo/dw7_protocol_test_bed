import re
import sys
import os
import traceback
import git
import json
from pathlib import Path
from datetime import datetime, timezone

# Define constants for the new data files
PENDING_EVENTS_FILE = "data/pending_events.json"
PROCESSED_EVENTS_FILE = "data/processed_events.json"
FAILURE_THRESHOLD = 3
STAGES = ["Engineer", "Researcher", "Coder", "Validator", "Deployer", "Rehearsal"]

class WorkflowKernel:
    def __init__(self, state):
        self.state = state
        self.current_stage = self.state.get("CurrentStage")
        self.python_executable_path = self.state.get("PythonExecutablePath")
        self.current_event = None

    def advance_stage(self, needs_research=False):
        self._reset_failure_counters(self.current_stage)

        # Explicit state transitions are more robust than index-based logic.
        if self.current_stage == "Rehearsal":
            next_stage = self.state.get("PreviousStage")
            self.state.delete("PreviousStage") # Clean up state
            if not next_stage:
                print("--- Governor: WARNING: PreviousStage not found. Defaulting to Engineer. ---", file=sys.stderr)
                next_stage = "Engineer"
        elif self.current_stage == "Engineer":
            next_stage = "Researcher" if needs_research else "Coder"
        elif self.current_stage == "Researcher":
            next_stage = "Coder"
        elif self.current_stage == "Coder":
            next_stage = "Validator"
        elif self.current_stage == "Validator":
            next_stage = "Deployer"
        elif self.current_stage == "Deployer":
            next_stage = "Engineer"
        else:
            raise Exception(f"Unknown stage transition from {self.current_stage}")

        self.state.set("CurrentStage", next_stage)
        if next_stage == "Engineer":
            self.state.increment("CycleCounter")
            self._complete_event_in_queue()
            self._advance_requirement_pointer()
            self._perform_context_refresh()
        self.state.save()
        print(f"--- Governor: Stage advanced from {self.current_stage} to {next_stage}. ---")

    def _handle_failure(self, exception):
        failure_key, current_failure_count = self._get_failure_context()
        
        if current_failure_count >= FAILURE_THRESHOLD:
            print(f"--- Governor: Failure threshold reached for {failure_key}. Escalating... ---", file=sys.stderr)
            new_req_id = self._create_red_flag_requirement(exception)
            if new_req_id:
                self.state.set("RequirementPointer", new_req_id)
                self.state.set("CurrentStage", "Engineer")
                self._reset_failure_counters(self.current_stage)
                self.state.save()
                print(f"--- Governor: Workflow reset to Engineer stage. Focus is now on {new_req_id}. ---")
            else:
                print("--- Governor: FATAL ERROR during escalation. Workflow halted. ---", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"--- Governor: Stage {self.current_stage} Approval Failed. Halting. ---", file=sys.stderr)

    def _get_failure_context(self):
        stage = self.current_stage
        failure_key = f"FailureCounters.{stage}.default"
        current_failure_count = self.state.increment(failure_key)
        return failure_key, current_failure_count

    def _reset_failure_counters(self, stage):
        # Simplified for now, can be expanded
        self.state.set(f"FailureCounters.{stage}.default", 0)
        self.state.save()

    def save_current_commit_sha(self):
        try:
            repo = git.Repo(search_parent_directories=True)
            self.state.set("Validator_CommitSHA", repo.head.commit.hexsha)
            self.state.save()
        except Exception as e:
            print(f"Error saving commit SHA: {e}", file=sys.stderr)

    def _complete_event_in_queue(self):
        try:
            with open(PENDING_EVENTS_FILE, "r") as f:
                pending_events = json.load(f)
            
            if not pending_events:
                print("--- Governor: No pending events to complete. ---")
                return

            # Move the completed event
            completed_event = pending_events.pop(0)
            completed_event['status'] = 'Deployed'
            completed_event['completed_at'] = datetime.now(timezone.utc).isoformat()

            with open(PROCESSED_EVENTS_FILE, "r+") as f:
                processed_events = json.load(f)
                processed_events.append(completed_event)
                f.seek(0)
                json.dump(processed_events, f, indent=2)
                f.truncate()

            # Update the pending events queue
            with open(PENDING_EVENTS_FILE, "w") as f:
                json.dump(pending_events, f, indent=2)

            print(f"--- Governor: Event {completed_event.get('id')} moved to processed queue. ---")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"--- Governor: Error processing event queues: {e}", file=sys.stderr)
        except Exception as e:
            print(f"--- Governor: Unexpected error completing event in queue: {e}", file=sys.stderr)

    def _advance_requirement_pointer(self):
        try:
            with open(PENDING_EVENTS_FILE, "r") as f:
                pending_events = json.load(f)

            if pending_events:
                next_event_summary = pending_events[0]
                req_id = next_event_summary.get("id")
                
                if req_id:
                    self.state.set("RequirementPointer", req_id)
                    self.state.save()
                    # Pass the full summary to the loader
                    self._load_event_details(next_event_summary)
                    print(f"--- Governor: RequirementPointer set to next event in queue: {req_id}. ---")
                else:
                    print(f"--- Governor: Error: Event in queue is missing an 'id'. ---", file=sys.stderr)
            else:
                print("--- Governor: No pending events found in the queue. ---")

        except FileNotFoundError:
            print(f"--- Governor: Error: Pending events file not found at {PENDING_EVENTS_FILE}. ---", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"--- Governor: Error: Could not decode JSON from {PENDING_EVENTS_FILE}. ---", file=sys.stderr)
        except Exception as e:
            print(f"Error advancing requirement pointer: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    def _load_event_details(self, event_summary):
        """Loads the full event data from the JSON file in the events/ directory."""
        event_id = event_summary.get("id")
        if not event_id:
            print(f"--- Governor: WARNING: Event summary is missing an 'id'. ---", file=sys.stderr)
            self.current_event = {"id": "Unknown", "title": "Details not found (missing ID)"}
            return

        event_file = Path(f"events/{event_id}.json")
        if event_file.exists():
            try:
                with open(event_file, "r", encoding='utf-8') as f:
                    self.current_event = json.load(f)
            except Exception as e:
                print(f"--- Governor: ERROR parsing event file {event_file}: {e} ---", file=sys.stderr)
                self.current_event = {"id": event_id, "title": f"Details not found (parsing error for {event_id})"}
        else:
            print(f"--- Governor: WARNING: Event file not found at {event_file} for {event_id} ---", file=sys.stderr)
            self.current_event = {"id": event_id, "title": f"Details not found (file missing for {event_id})"}

    def create_new_requirement(self, requirement_id, title, description, acceptance_criteria):
        """Creates a new requirement file and adds it to the pending events queue."""
        print(f"--- Governor: Creating new requirement: {requirement_id} ---")

        # Create the detailed JSON event file
        event_data = {
            "id": requirement_id,
            "title": title,
            "description": description,
            "acceptance_criteria": [{"text": ac, "completed": False} for ac in acceptance_criteria],
            "status": "Pending",
            "priority": "Medium",
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        event_path = Path(f"events/{requirement_id}.json")
        event_path.parent.mkdir(parents=True, exist_ok=True)
        with open(event_path, "w", encoding='utf-8') as f:
            json.dump(event_data, f, indent=2)

        # Create a summary event for the pending queue
        event_summary = {
            "id": requirement_id,
            "title": title,
            "status": "Pending",
            "priority": "Medium",
            "created_at": event_data["created_at"]
        }

        # Append summary to pending_events.json
        try:
            with open(PENDING_EVENTS_FILE, "r+") as f:
                pending_events = json.load(f)
                pending_events.append(event_summary)
                f.seek(0)
                json.dump(pending_events, f, indent=2)
                f.truncate()
        except (FileNotFoundError, json.JSONDecodeError):
            with open(PENDING_EVENTS_FILE, "w") as f:
                json.dump([event_summary], f, indent=2)
        
        print(f"--- Governor: Successfully created {requirement_id} and added to event queue. ---")

    def _perform_context_refresh(self):
        print("\n--- Governor: Performing Mandatory Context Refresh ---")
        if not self.current_event:
            print("--- Governor: No active event loaded. Cannot refresh context. ---", file=sys.stderr)
            return

        print(f"\n*** Active Event ({self.current_event.get('id')}) ***")
        print(f"Title: {self.current_event.get('title')}")
        print(f"Description: {self.current_event.get('description')}")
        print("Acceptance Criteria:")
        for i, smr in enumerate(self.current_event.get('acceptance_criteria', [])):
            status = "[x]" if smr.get('completed') else "[ ]"
            print(f"  {i+1}. {status} {smr.get('text')}")

        tutorial_file = "docs/AI_PROTOCOL_TUTORIAL.md"
        if os.path.exists(tutorial_file):
            print(f"\n*** AI Protocol Tutorial ({os.path.basename(tutorial_file)}) ***")
            with open(tutorial_file, "r") as f:
                print(f.read())
        print("\n--- Context Refresh Complete ---\n")

    def _create_red_flag_requirement(self, exception):
        try:
            # Determine the next requirement ID by checking both queues
            all_ids = []
            for event_file in [PENDING_EVENTS_FILE, PROCESSED_EVENTS_FILE]:
                try:
                    with open(event_file, "r") as f:
                        events = json.load(f)
                        all_ids.extend([int(num) for event in events for num in re.findall(r'REQ-DW8-(\d+)', event.get('id', '')) if num])
                except (FileNotFoundError, json.JSONDecodeError, ValueError):
                    pass  # Ignore if file doesn't exist, is empty/invalid, or contains non-matching IDs

            next_id = max(all_ids) + 1 if all_ids else 1
            new_req_id = f"REQ-DW8-{next_id:03d}"

            # Create the detailed red flag requirement file
            red_flag_path = f"docs/reqs/{new_req_id}.md"
            exc_type = type(exception).__name__
            exc_message = str(exception).replace('\n', '\n    ')
            tb_str = "".join(traceback.format_tb(exception.__traceback__)).replace('\n', '\n      ')

            red_flag_content = f"""### ID: {new_req_id}

- **Title:** Red Flag: Unhandled Critical Failure in {self.current_stage} Stage
- **Status:** `Pending`
- **Priority:** `Critical`
- **Details:** The workflow encountered a critical failure after multiple retries. The system has been reset to the Engineer stage to re-evaluate the approach.
- **SMRs:**
  - [ ] Analyze the failure context below to understand the root cause.
  - [ ] Formulate a new plan to address the failure.
  - [ ] Implement the new plan.
- **Failure Context:**
  - **Exception Type:** `{exc_type}`
  - **Exception Message:**
    ```
    {exc_message}
    ```
  - **Traceback:**
    ```
    {tb_str}
    ```
"""
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
            try:
                with open(PENDING_EVENTS_FILE, "r+") as f:
                    pending_events = json.load(f)
                    pending_events.insert(0, new_event)
                    f.seek(0)
                    json.dump(pending_events, f, indent=2)
                    f.truncate()
            except (FileNotFoundError, json.JSONDecodeError):
                with open(PENDING_EVENTS_FILE, "w") as f:
                    json.dump([new_event], f, indent=2)

            print(f"Successfully injected {new_req_id} into {PENDING_EVENTS_FILE}")

            return new_req_id

        except Exception as e:
            print(f"FATAL: Could not create Red Flag requirement. Error: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return None

