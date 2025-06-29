import sys
from datetime import datetime

def _display_startup_summary(self):
    """
    Displays a personalized startup message including the user's name,
    time since last session, and a summary of the current project status.
    """
    if not hasattr(self, 'user_profile'):
        print("--- Governor: User profile not loaded. Skipping startup summary. ---", file=sys.stderr)
        return

    user_name = self.user_profile.get("user_name", "User")
    last_session_str = self.user_profile.get("last_session_timestamp")

    time_since_last_session = "this is your first session"
    if last_session_str:
        try:
            last_session_dt = datetime.fromisoformat(last_session_str)
            # Use a timezone-unaware current time to match the stored ISO format
            now = datetime.now()
            delta = now - last_session_dt.replace(tzinfo=None)

            seconds = delta.total_seconds()
            if seconds < 60:
                time_since_last_session = f"{int(seconds)} seconds ago"
            elif seconds < 3600:
                time_since_last_session = f"{int(seconds / 60)} minutes ago"
            elif seconds < 86400:
                time_since_last_session = f"{int(seconds / 3600)} hours ago"
            else:
                time_since_last_session = f"{int(seconds / 86400)} days ago"
        except (ValueError, TypeError):
            time_since_last_session = "an unknown time ago"

    print("\n--- DW8 Workflow Initialized ---")
    print(f"Welcome back, {user_name}. Your last session was {time_since_last_session}.")
    print("----------------------------------")

    current_req = self.state.get("RequirementPointer", "N/A")
    current_stage = self.state.get("CurrentStage", "N/A")
    print(f"Active Requirement: {current_req}")
    print(f"Current Stage: {current_stage}")
    print("----------------------------------\n")
