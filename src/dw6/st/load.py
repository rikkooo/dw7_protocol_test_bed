import json
import sys
from pathlib import Path

def load(self):
    # One-time migration from old format
    old_state_file = Path('.workflow_state')
    if old_state_file.exists() and not self.state_file.exists():
        print(f"--- Governor: Migrating state from {old_state_file} to {self.state_file} ---")
        temp_data = {}
        with open(old_state_file, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    temp_data[key] = value
        self.data = temp_data
        self.save()
        old_state_file.unlink() # Remove old file after successful migration
        return

    if self.state_file.exists() and self.state_file.stat().st_size > 0:
        try:
            with open(self.state_file, "r") as f:
                self.data = json.load(f)
        except json.JSONDecodeError:
            print(f"--- Governor: WARNING: Could not decode JSON from {self.state_file}. Re-initializing. ---", file=sys.stderr)
            self.initialize_state()
    else:
        self.initialize_state()

    # Data migration for CognitiveCheckpoint
    if "CognitiveCheckpoint" not in self.data:
        print("--- Governor: Migrating state to include CognitiveCheckpoint. ---")
        self.data["CognitiveCheckpoint"] = "Riko"
        self.save() # Persist the migrated state

    # Data migration for statistics
    if "statistics" not in self.data:
        print("--- Governor: Migrating state to include statistics tracking. ---")
        self.data["statistics"] = {
            "total_requirements_completed": 0,
            "total_requirements_pending": 0,
            "failure_rates_by_stage": {}
        }
        self.save()

    # Data migration for is_protocol_update flag
    if "is_protocol_update" not in self.data:
        print("--- Governor: Migrating state to include is_protocol_update flag. ---")
        self.data["is_protocol_update"] = False
        self.save()
