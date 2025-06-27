class CoderStage:
    def __init__(self, state):
        self.state = state

    def validate(self, allow_failures=False):
        # No specific validation for the Coder stage at this time.
        return True
