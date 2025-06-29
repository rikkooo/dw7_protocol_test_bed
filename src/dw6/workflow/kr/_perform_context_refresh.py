import os
import sys

def _perform_context_refresh(self):
    """
    Displays a detailed status report of the current workflow state, including
    the active requirement's details and the AI Protocol Tutorial.
    This method serves as the primary output for the `dw6 status` command.
    """
    print("--- DW7 Workflow Status ---")
    print(f"Cycle: {self.state.get('CycleCounter', 'N/A')}")
    print(f"Current Stage: {self.current_stage}")

    if not self.current_event:
        print("Requirement ID: Not available (no event loaded)")
        print("---------------------------")
        return

    title = self.current_event.get('title')
    description = self.current_event.get('description')



    acceptance_criteria = self.current_event.get('acceptance_criteria', [])

    print(f"Title: {title}")
    print(f"Description: {description}")
    print("Acceptance Criteria:")
    if acceptance_criteria:
        for i, smr in enumerate(acceptance_criteria):
            status = "[x]" if smr.get('completed') else "[ ]"
            print(f"  {i+1}. {status} {smr.get('text')}")
    else:
        print("  (No acceptance criteria specified)")

    print("---------------------------")

    # Also print the AI Protocol Tutorial for context
    tutorial_file = "docs/AI_PROTOCOL_TUTORIAL.md"
    if os.path.exists(tutorial_file):
        print(f"\n*** AI Protocol Tutorial ({os.path.basename(tutorial_file)}) ***")
        with open(tutorial_file, "r") as f:
            print(f.read())
