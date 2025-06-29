import sys

def authorize(self, command: str):
    """Checks if a command is allowed in the current stage."""
    # Access RULES via self.__class__ because it's a class attribute
    allowed_commands = self.__class__.RULES.get(self.current_stage, [])
    if not any(command.startswith(prefix) for prefix in allowed_commands):
        print(f"--- Governor: Command '{command}' is not authorized in the '{self.current_stage}' stage. ---", file=sys.stderr)
        return False
    return True
