import os
from dotenv import load_dotenv, find_dotenv

def _load_environment(self):
    # REQ-DW8-017-01: Implement Strict Environment Variable Loading
    env_path = find_dotenv()
    if not env_path:
        raise FileNotFoundError("--- Governor: CRITICAL: .env file not found. The workflow cannot proceed without environment configuration. ---")
    load_dotenv(dotenv_path=env_path)
    print("--- Governor: .env file loaded successfully. ---")

    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("--- Governor: CRITICAL: GITHUB_TOKEN not found in the environment. Please ensure it is set in the .env file. ---")
