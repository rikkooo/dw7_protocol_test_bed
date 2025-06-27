import json
import re
import os

# Define paths relative to the script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

SOURCE_MD_PATH = os.path.join(PROJECT_ROOT, 'docs', 'PROJECT_REQUIREMENTS.md')
PENDING_JSON_PATH = os.path.join(PROJECT_ROOT, 'data', 'pending_events.json')
PROCESSED_JSON_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed_events.json')

# Regex to capture the components of a requirement line
REQ_PATTERN = re.compile(r'^\[([PD])\] \[([CHML])\] \[(REQ-DW8-.*?)\] (.*?) -> (\./.*?\.md)$')

def migrate_requirements():
    """
    Parses the Markdown requirements file and migrates the entries
    to the corresponding JSON event queues.
    """
    pending_events = []
    processed_events = []

    print(f"Reading from {SOURCE_MD_PATH}...")
    try:
        with open(SOURCE_MD_PATH, 'r') as f:
            for line in f:
                match = REQ_PATTERN.match(line.strip())
                if match:
                    status_char, priority_char, req_id, title, path = match.groups()

                    # Map characters to full text
                    status = 'Deployed' if status_char == 'D' else 'Pending'
                    priority_map = {'C': 'Critical', 'H': 'High', 'M': 'Medium', 'L': 'Low'}
                    priority = priority_map.get(priority_char, 'Unknown')

                    event = {
                        'id': req_id,
                        'title': title.strip(),
                        'status': status,
                        'priority': priority,
                        'path': path
                    }

                    if status == 'Deployed':
                        processed_events.append(event)
                    else:
                        pending_events.append(event)

    except FileNotFoundError:
        print(f"Error: Source file not found at {SOURCE_MD_PATH}")
        return

    # Write to JSON files
    print(f"Writing {len(pending_events)} events to {PENDING_JSON_PATH}")
    with open(PENDING_JSON_PATH, 'w') as f:
        json.dump(pending_events, f, indent=2)

    print(f"Writing {len(processed_events)} events to {PROCESSED_JSON_PATH}")
    with open(PROCESSED_JSON_PATH, 'w') as f:
        json.dump(processed_events, f, indent=2)

    print("Migration complete.")

if __name__ == '__main__':
    migrate_requirements()
