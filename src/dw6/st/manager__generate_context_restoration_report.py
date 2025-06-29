def _generate_context_restoration_report(self):
    """Generates a summary of the restored context for user verification."""
    restored_context = self.state.get("__temp_restored_context", "No context was restored.")
    print("--- Governor: CONTEXT RESTORATION REPORT ---")
    print(restored_context)
    print("--- END OF REPORT ---")
    self.state.delete("__temp_restored_context") # Clean up temp state
