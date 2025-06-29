import os
import json

def compile_events(events_dir, output_file):
    """Compiles all individual event JSON files into a single master JSON file."""
    all_events = []
    if not os.path.exists(events_dir):
        print(f"Error: Events directory not found at '{events_dir}'")
        return

    for filename in sorted(os.listdir(events_dir)):
        if filename.endswith('.json'):
            file_path = os.path.join(events_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    event_data = json.load(f)
                    all_events.append(event_data)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {filename}. Skipping.")
            except Exception as e:
                print(f"Warning: Could not read {filename}. Error: {e}. Skipping.")

    with open(output_file, 'w') as f:
        json.dump(all_events, f, indent=2)
    
    print(f"Event ledger successfully compiled at {output_file}")

if __name__ == "__main__":
    # Assuming the script is run from the project root
    events_directory = "events"
    output_json_file = "docs/EVENTS.json"
    compile_events(events_directory, output_json_file)
