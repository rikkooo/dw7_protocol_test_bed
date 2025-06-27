import os
import re
import json

# Define paths
REQS_DIR = 'docs/reqs'
EVENTS_DIR = 'events'

def parse_md_file(file_path):
    """Parses a single Markdown requirement file and extracts its data."""
    with open(file_path, 'r') as f:
        content = f.read()

    data = {}
    
    # More robust regex to capture ID and Title from various header formats
    # Handles formats like:
    # - # REQ-DW8-OS-007: [Execution] Refactor Requirement Files to JSON Events
    # - # REQ-DW8-002 Implement the Rehearsal State
    # - # REQ-DW8-012
    title_match = re.search(r'#\s*(REQ-DW8-.*?)(?::\s*\[.*?\])?\s*(.*)', content)
    if title_match:
        data['id'] = title_match.group(1).strip()
        data['title'] = title_match.group(2).strip() if title_match.group(2) else "No title found"
    else:
        # Fallback for files where the main regex fails
        id_match_fallback = re.search(r'(REQ-DW8-\d+)', file_path)
        if id_match_fallback:
            data['id'] = id_match_fallback.group(1)
            data['title'] = "Title requires manual entry"
        else:
            return None # Cannot proceed without an ID

    # Extract metadata from the list
    priority_match = re.search(r'-\s*\*\*Priority:\*\*\s*\[(.)\]', content)
    if priority_match:
        priority_map = {'C': 'Critical', 'H': 'High', 'M': 'Medium', 'L': 'Low'}
        data['priority'] = priority_map.get(priority_match.group(1), 'Unknown')

    status_match = re.search(r'-\s*\*\*Status:\*\*\s*\[(.)\]', content)
    if status_match:
        status_map = {'P': 'Pending', 'D': 'Deployed'}
        data['status'] = status_map.get(status_match.group(1), 'Unknown')

    type_match = re.search(r'-\s*\*\*Type:\*\*\s*(.*)', content)
    if type_match:
        data['type'] = type_match.group(1).strip()

    # Extract Description
    description_match = re.search(r'## 1\.\s*Description\n\n(.*?)\n\n## 2\.\s*', content, re.DOTALL)
    if description_match:
        data['description'] = description_match.group(1).strip()

    # Extract Acceptance Criteria (SMRs)
    smrs = []
    smr_matches = re.findall(r'-\s*\[( |x)\]\s*(.*)', content)
    for smr in smr_matches:
        smrs.append({
            "completed": smr[0] == 'x',
            "text": smr[1].strip()
        })
    data['acceptance_criteria'] = smrs
    
    data['source_file'] = file_path

    return data

def convert_all_reqs_to_events():
    """
    Converts all Markdown requirement files in docs/reqs/
    to JSON event files in events/.
    """
    if not os.path.exists(EVENTS_DIR):
        print(f"Creating directory: {EVENTS_DIR}")
        os.makedirs(EVENTS_DIR)

    print(f"Scanning for requirement files in {REQS_DIR}...")
    converted_count = 0
    skipped_count = 0
    for filename in os.listdir(REQS_DIR):
        if filename.endswith('.md'):
            md_path = os.path.join(REQS_DIR, filename)
            try:
                event_data = parse_md_file(md_path)
                if event_data and 'id' in event_data:
                    json_filename = f"{event_data['id']}.json"
                    json_path = os.path.join(EVENTS_DIR, json_filename)
                    
                    with open(json_path, 'w') as f:
                        json.dump(event_data, f, indent=2)
                    
                    print(f"  - Converted {filename} -> {json_filename}")
                    converted_count += 1
                else:
                    print(f"  - WARNING: Could not extract a valid ID from {filename}. Skipping.")
                    skipped_count += 1
            except Exception as e:
                print(f"  - ERROR: Failed to process {filename}: {e}")
                skipped_count += 1

    print(f"\nConversion complete. {converted_count} files converted, {skipped_count} files skipped.")

if __name__ == '__main__':
    convert_all_reqs_to_events()