# /usr/bin/env python
import os

class Governor:
    """The master controller and protocol enforcer for the DW8 system."""

    def __init__(self, start_path: str = None):
        """Initializes the Governor."""
        self.start_path = start_path
        print("Governor initialized.")

    def start_session(self, requirement_id: str):
        """Starts a new work session for a given requirement."""
        print(f"Starting session for requirement: {requirement_id}")
        # Placeholder for state transition logic
        pass

    def approve_stage(self):
        """Approves the current stage and transitions to the next."""
        print("Current stage approved.")
        # Placeholder for validation and state transition logic
        pass

    def _find_and_load_context(self, start_path: str) -> str:
        """Traverses up from start_path to find and read a _CONTEXT.md file."""
        current_path = os.path.abspath(start_path)
        if not os.path.isdir(current_path):
            current_path = os.path.dirname(current_path)

        while True:
            context_file = os.path.join(current_path, "_CONTEXT.md")
            if os.path.exists(context_file):
                print(f"Found context file: {context_file}")
                with open(context_file, 'r', encoding='utf-8') as f:
                    return f.read()

            # Move up one directory
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:  # Reached the root directory
                return ""
            current_path = parent_path

if __name__ == '__main__':
    # Test the context loading from a deep path
    test_path = '/home/ubuntu/devs/dw7_protocol_test_bed/src/dw6/workflow/kr/main.py'
    gov = Governor()
    context = gov._find_and_load_context(test_path)
    
    if context:
        print("\n--- Context Loaded ---")
        print(context)
        print("----------------------")
    else:
        print("No context file found.")
