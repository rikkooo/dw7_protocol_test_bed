import os
import re
import json
from pathlib import Path

SOURCE_DIR = Path("docs/reqs")
DEST_DIR = Path("events")

def migrate_requirements():
    """Migrates requirement files from Markdown to JSON format."""
    if not SOURCE_DIR.exists():
        print(f"Source directory not found: {SOURCE_DIR}")
        return

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Migrating .md files from {SOURCE_DIR} to .json files in {DEST_DIR}...")

    for md_file in SOURCE_DIR.glob("*.md"):
        try:
            with open(md_file, "r", encoding='utf-8') as f:
                content = f.read()

            # Extract data using regex
            req_id, title = None, None

            # Strategy 1: H1 header format (e.g., # REQ-ID: Title)
            h1_match = re.search(r'^#.*(REQ-DW8-[\w-]+):(.*)', content, re.MULTILINE)
            if h1_match:
                req_id, title = h1_match.groups()

            # Strategy 2: Markdown list format (e.g., ### ID: REQ-ID, - **Title:** Title)
            if not req_id:
                id_match = re.search(r'^##+\s*ID:\s*(REQ-DW8-[\w-]+)', content, re.MULTILINE)
                title_match_list = re.search(r'^-\s*\*\*Title:\*\*\s*(.*)', content, re.MULTILINE)
                if id_match and title_match_list:
                    req_id = id_match.group(1)
                    title = title_match_list.group(1)

            if not req_id or not title:
                print(f"Could not parse title or ID from {md_file}. Skipping.")
                continue

            title = title.strip()
            req_id = req_id.strip()

            description_match = re.search(r'##\s*1\.\s*Description\s*\n\s*(.*?)\n\s*##', content, re.DOTALL)
            description = description_match.group(1).strip() if description_match else ""

            ac_match = re.search(r'##\s*2\.\s*Acceptance\s*Criteria\s*\n\s*(.*)', content, re.DOTALL)
            acceptance_criteria = []
            if ac_match:
                ac_text = ac_match.group(1)
                criteria_lines = re.findall(r'-\s*\[ \]\s*(.*)', ac_text)
                for line in criteria_lines:
                    acceptance_criteria.append({"text": line.strip(), "completed": False})

            # Create JSON structure
            json_data = {
                "id": req_id,
                "title": title,
                "description": description,
                "acceptance_criteria": acceptance_criteria,
                "status": "Pending", # Default status
                "priority": "Medium" # Default priority
            }

            # Write JSON file
            json_file_path = DEST_DIR / f"{req_id}.json"
            with open(json_file_path, "w", encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            
            print(f"Successfully migrated {md_file.name} to {json_file_path.name}")

        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

    print("Migration complete.")

if __name__ == '__main__':
    migrate_requirements()
