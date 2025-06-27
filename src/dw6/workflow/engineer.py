import re
import sys

REQUIREMENTS_FILE = "docs/PROJECT_REQUIREMENTS.md"

class EngineerStage:
    def __init__(self, state):
        self.state = state

    def validate(self, allow_failures=False):
        """Ensures the current requirement is broken down into atomic sub-tasks."""
        print("--- Governor: Checking for atomic requirement... ---")
        try:
            req_pointer = self.state.get("RequirementPointer")
            if not req_pointer:
                print("RequirementPointer not found in state. Skipping check.")
                return True

            req_id = req_pointer
            print(f"Current requirement ID: {req_id}")

            with open(REQUIREMENTS_FILE, "r") as f:
                content = f.read()

            match = re.search(rf"(?s)### ID: {re.escape(req_id)}\n(.*?)(?=\n---\n|\Z)", content)

            if match:
                requirement_text = match.group(1).strip()
                smr_section_match = re.search(r"- \*\*SMRs:\*\*\n((?:  - .+\n?)+)", requirement_text, re.MULTILINE)

                if smr_section_match:
                    smr_block = smr_section_match.group(1)
                    smr_count = len(re.findall(r"^  - \[", smr_block, re.MULTILINE))
                    print(f"Found {smr_count} SMRs.")

                    if smr_count < 2:
                        print("\n[GOVERNOR] HALT: Requirement is not sufficiently granular.", file=sys.stderr)
                        print("Please break it down into at least two sub-tasks using 'dw6 breakdown <REQ_ID>'.", file=sys.stderr)
                        return False
            
            print("--- Governor: Atomic requirement check passed. ---")
            return True

        except Exception as e:
            print(f"Error during atomic requirement check: {e}", file=sys.stderr)
            raise e
