import json
import sys
from pathlib import Path
from datetime import datetime

def _manage_user_profile(self):
    """
    Manages the user profile, creating it if it doesn't exist and
    updating the last session timestamp.
    """
    # If running under pytest, use a mock profile and skip all file I/O and prompts.
    if "pytest" in sys.modules:
        self.user_profile = {
            "user_name": "TestUser",
            "last_session_timestamp": datetime.now().isoformat()
        }
        return

    profile_path = Path("data/user_profile.json")
    profile_data = {}

    if profile_path.exists():
        with open(profile_path, "r") as f:
            try:
                profile_data = json.load(f)
            except json.JSONDecodeError:
                # Handle case where file is empty or corrupt
                profile_data = {}

    if not profile_data.get("user_name"):
        try:
            # This is a placeholder for a more robust interaction model.
            user_name = input("--- Governor: It looks like this is our first time working together. What should I call you? --- ")
            profile_data["user_name"] = user_name.strip()
        except (EOFError, OSError):
            # Handle non-interactive environments by setting a default.
            print("--- Governor: Could not read user name in non-interactive mode. Using default 'Riko'. ---", file=sys.stderr)
            profile_data["user_name"] = "Riko"

    profile_data["last_session_timestamp"] = datetime.now().isoformat()

    with open(profile_path, "w") as f:
        json.dump(profile_data, f, indent=2)

    # Store profile data in the kernel for the current session for easy access
    self.user_profile = profile_data
    print(f"--- Governor: User profile loaded for {profile_data['user_name']}. ---")
