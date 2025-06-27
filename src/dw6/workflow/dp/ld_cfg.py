import sys
from pathlib import Path

def _load_config(self):
    config = {}
    config_path = Path("docs/DEPLOYER_CONFIGURATION.md")
    if not config_path.exists():
        print(f"--- Governor: WARNING: {config_path} not found. Deployer may not function correctly. ---", file=sys.stderr)
        return config

    with open(config_path, "r") as f:
        for line in f:
            if ":" in line:
                key, value = line.split(":", 1)
                config[key.strip()] = value.strip()
    return config
