import sys

def check_context(self):
    """Performs a context integrity check."""
    print("--- Governor: Performing Context Integrity Check... ---")
    
    # SMR-2: Cognitive Checkpoint
    cognitive_checkpoint = self.state.get("CognitiveCheckpoint")
    if cognitive_checkpoint != "Riko":
        print("--- Governor: CRITICAL: Cognitive Checkpoint mismatch. Expected 'Riko'. ---", file=sys.stderr)
        print("--- Governor: Context is considered unstable. Performing full context refresh. ---", file=sys.stderr)
        self._perform_context_refresh_procedure()
        self._generate_context_restoration_report()
    else:
        print("--- Governor: Cognitive Checkpoint is stable. ---")
