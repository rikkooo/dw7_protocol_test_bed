from pathlib import Path

def _check_if_project_is_complete(self):
    """Checks if all requirements in the master list are marked as Deployed."""
    reqs_path = Path("docs/PROJECT_REQUIREMENTS.md")
    if not reqs_path.exists():
        return False

    with open(reqs_path, "r") as f:
        content = f.read()

    req_lines = [line for line in content.split('\n') if "REQ-" in line]
    if not req_lines:
        return False

    for line in req_lines:
        if not line.strip().startswith("[D]"):
            return False

    return True
