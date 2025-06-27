import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import os
from datetime import datetime
from dw6.state_manager import WorkflowState, WorkflowManager
from dw6.templates import TECHNICAL_SPECIFICATION_TEMPLATE

def main():
    parser = argparse.ArgumentParser(
        description="DW5-Preview: A modern, robust development workflow."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'new' command
    new_parser = subparsers.add_parser("new", help="Start a new development cycle for a requirement.")
    new_parser.add_argument("requirement_id", type=str, help="The ID of the requirement to work on.")
    new_parser.add_argument("-t", "--title", required=True, help="Title of the requirement.")
    new_parser.add_argument("-d", "--description", required=True, help="Detailed description of the requirement.")
    new_parser.add_argument("-a", "--acceptance-criteria", required=True, nargs='+', help="List of acceptance criteria.")

    # 'approve' command
    approve_parser = subparsers.add_parser("approve", help="Approve the current stage and advance to the next.")

    # 'meta-req' command
    meta_req_parser = subparsers.add_parser("meta-req", help="Manage meta-requirements.")
    meta_req_subparsers = meta_req_parser.add_subparsers(dest="meta_command", required=True)
    
    # 'meta-req new' command
    new_meta_parser = meta_req_subparsers.add_parser("new", help="Create a new meta-requirement.")
    new_meta_parser.add_argument("-t", "--title", required=True, help="Title of the meta-requirement.")
    new_meta_parser.add_argument("-d", "--details", required=True, help="Detailed description of the requirement.")
    new_meta_parser.add_argument("-p", "--priority", required=True, choices=["Critical", "High", "Medium", "Low"], help="Priority of the requirement.")

    args = parser.parse_args()
    state = WorkflowState()
    manager = WorkflowManager(state)

    if args.command == "new":
        manager.create_new_requirement(
            args.requirement_id,
            args.title,
            args.description,
            args.acceptance_criteria
        )
    elif args.command == "approve":
        manager.approve()
    elif args.command == "meta-req":
        if args.meta_command == "new":
            manager.create_new_meta_requirement(args.title, args.details, args.priority)

if __name__ == "__main__":
    main()
