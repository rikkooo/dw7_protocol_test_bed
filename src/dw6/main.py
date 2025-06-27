# dw6/main.py
import argparse
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from dw6.state_manager import WorkflowManager, WorkflowState, STAGES
from dw6.augmenter import PromptAugmenter
from dw6.templates import process_prompt

META_LOG_FILE = Path("logs/meta_requirements.log")
TECH_DEBT_FILE = Path("logs/technical_debt.log")

def register_meta_requirement(description: str):
    """Logs a new meta-requirement to the meta_requirements.log file."""
    META_LOG_FILE.parent.mkdir(exist_ok=True)
    
    last_id = 0
    if META_LOG_FILE.exists():
        with open(META_LOG_FILE, "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                match = re.search(r'^\[ID:(\d+)\]', last_line)
                if match:
                    last_id = int(match.group(1))

    new_id = last_id + 1
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = f"[ID:{new_id}] [TS:{timestamp}] {description}\n"

    with open(META_LOG_FILE, "a") as f:
        f.write(log_entry)
    
    print(f"Successfully logged meta-requirement {new_id}.")

def register_technical_debt(description, issue_type="test", commit_to_fix=None):
    """Registers a known technical debt item for future resolution."""
    TECH_DEBT_FILE.parent.mkdir(exist_ok=True)
    
    last_id = 0
    if TECH_DEBT_FILE.exists():
        with open(TECH_DEBT_FILE, "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                match = re.search(r'^\[ID:(\d+)\]', last_line)
                if match:
                    last_id = int(match.group(1))

    new_id = last_id + 1
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    status = "OPEN"
    log_entry = f"[ID:{new_id}] [TS:{timestamp}] [TYPE:{issue_type}] [STATUS:{status}] "
    if commit_to_fix:
        log_entry += f"[COMMIT:{commit_to_fix}] "
    log_entry += f"{description}\n"

    with open(TECH_DEBT_FILE, "a") as f:
        f.write(log_entry)
    
    print(f"Successfully logged technical debt {new_id}.")
    return new_id

def revert_to_previous_stage(manager, target_stage=None):
    """Reverts the workflow to a previous stage."""
    try:
        manager.revert_stage(target_stage)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

def handle_status(manager):
    """Handles the status command."""
    state = manager.state
    current_stage = state.get("CurrentStage", "Unknown")
    requirement_pointer = state.get("RequirementPointer", "Unknown")
    cycle_counter = state.get("CycleCounter", "Unknown")

    print(f"--- DW7 Workflow Status ---")
    print(f"Cycle: {cycle_counter}")
    print(f"Current Stage: {current_stage}")
    print(f"Requirement ID: {requirement_pointer}")

    try:
        with open("dw7_validation_report.md", "r") as f:
            content = f.read()
        
        # Use regex to find the requirement description
        match = re.search(f"## Finding {requirement_pointer}:(.*?)\n", content)
        if match:
            requirement_title = match.group(1).strip()
            print(f"Requirement: {requirement_title}")
        else:
            print("Requirement description not found in validation report.")

    except FileNotFoundError:
        print("Validation report not found.")
    print("---------------------------")

def main():
    """Main entry point for the DW6 CLI."""
    parser = argparse.ArgumentParser(description="DW6 Workflow Management Tool")
    subparsers = parser.add_subparsers(dest="command", help='Available commands')

    # Approve command
    approve_parser = subparsers.add_parser("approve", help="Approve the current stage and advance to the next.")
    approve_parser.add_argument("--allow-failures", action="store_true", help="Approve even if validation checks fail.")
    approve_parser.add_argument("--needs-research", action="store_true", help="Transition to the Researcher stage instead of Coder.")

    # New command
    new_parser = subparsers.add_parser("new", help="Create a new deliverable based on a prompt.")
    new_parser.add_argument("prompt", type=str, help="The prompt to generate the deliverable from.")

    # Meta-req command
    meta_req_parser = subparsers.add_parser("meta-req", help="Register a new meta-requirement for the workflow.")
    meta_req_parser.add_argument("description", type=str, help="The description of the meta-requirement.")

    # Tech-debt command
    tech_debt_parser = subparsers.add_parser("tech-debt", help="Register a technical debt item.")
    tech_debt_parser.add_argument("description", type=str, help="Description of the technical debt.")
    tech_debt_parser.add_argument("--type", default="test", help="Type of technical debt (e.g., test, code, deployment)")
    tech_debt_parser.add_argument("--commit", help="Commit hash where this should be fixed")

    # Revert command
    revert_parser = subparsers.add_parser("revert", help="Revert to a previous workflow stage.")
    revert_parser.add_argument("--to", dest="target_stage", help="Target stage to revert to. Defaults to previous stage.")

    # Do command
    do_parser = subparsers.add_parser("do", help="Execute a governed action.")
    do_parser.add_argument("action", type=str, help="The action to execute.")

    # Status command
    status_parser = subparsers.add_parser("status", help="Display the current workflow status.")

    # Breakdown command
    breakdown_parser = subparsers.add_parser("breakdown", help="Break down a requirement into sub-tasks.")
    breakdown_parser.add_argument("req_id", type=str, help="The ID of the requirement to break down (e.g., REQ-DW8-012).")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    state = WorkflowState()
    manager = WorkflowManager(state)
    
    if args.command == "meta-req":
        register_meta_requirement(args.description)
    elif args.command == "tech-debt":
        register_technical_debt(args.description, args.type, args.commit)
    elif args.command == "revert":
        revert_to_previous_stage(manager, args.target_stage)
    elif args.command == "do":
        try:
            manager.governor.authorize(args.action)
            # The command is authorized. The gatekeeper's job is done.
        except PermissionError:
            sys.exit(1)
    elif args.command == "approve":
        manager.approve(allow_failures=args.allow_failures, needs_research=args.needs_research)
    elif args.command == "new":
        cycle_counter = manager.state.get("CycleCounter")
        augmenter = PromptAugmenter()
        augmented_prompt = augmenter.augment_prompt(args.prompt)
        process_prompt(augmented_prompt, cycle_counter)
    elif args.command == "status":
        handle_status(manager)
    elif args.command == "breakdown":
        handle_breakdown(manager, args.req_id)

def handle_breakdown(manager, req_id):
    if manager.state.get("CurrentStage") != "Engineer":
        print("Error: The 'breakdown' command can only be used in the Engineer stage.", file=sys.stderr)
        sys.exit(1)

    print(f"--- Starting breakdown for {req_id} ---")
    print("Enter Sub-Meta-Requirements (SMRs) one by one. Type 'done' when finished.")
    
    smrs = []
    while True:
        smr = input(f"SMR {len(smrs) + 1}: ")
        if smr.lower() == 'done':
            break
        smrs.append(smr)

    if not smrs:
        print("No SMRs entered. Aborting.")
        return

    try:
        with open("docs/PROJECT_REQUIREMENTS.md", "r+") as f:
            content = f.read()
            
            # Find the requirement and replace the SMR section
            req_pattern = rf"(### ID: {re.escape(req_id)}\n(?:(?!- \*\*SMRs:\*\*).)*\n- \*\*SMRs:\*\*\n)((?:  - \[ \].*\n)*)"
            match = re.search(req_pattern, content, re.DOTALL)

            if not match:
                print(f"Error: Could not find requirement {req_id} with an SMR section to update.", file=sys.stderr)
                return

            start_of_smr_block = match.group(1)
            new_smr_block = "".join([f"  - [ ] {s}\n" for s in smrs])
            
            updated_content = content.replace(match.group(0), start_of_smr_block + new_smr_block)
            
            f.seek(0)
            f.write(updated_content)
            f.truncate()

        print(f"Successfully updated {req_id} with {len(smrs)} SMRs.")

    except FileNotFoundError:
        print("Error: docs/PROJECT_REQUIREMENTS.md not found.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
