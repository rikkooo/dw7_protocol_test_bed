import json

def save(self):
    self.state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(self.state_file, "w") as f:
        json.dump(self.data, f, indent=2, sort_keys=True)
