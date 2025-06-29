def show_status(self):
    """Displays the context of the current event and stage."""
    self.kernel._perform_context_refresh()
