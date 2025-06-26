import argparse
from .state_manager import WorkflowManager

def main():
    parser = argparse.ArgumentParser(description="A robust development workflow manager.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'new' command: Start a new development cycle for a requirement
    new_parser = subparsers.add_parser("new", help="Start a new development cycle for a requirement.")
    new_parser.add_argument("requirement_id", type=str, help="The ID of the requirement to work on.")

    # 'approve' command: Approve the current stage and advance to the next
    approve_parser = subparsers.add_parser("approve", help="Approve the current stage and advance to the next.")

    # 'set-stage' command: Manually set the current workflow stage
    set_stage_parser = subparsers.add_parser("set-stage", help="Manually set the current workflow stage.")
    set_stage_parser.add_argument("stage", type=str, help="The stage to set as current.")

    args = parser.parse_args()
    manager = WorkflowManager()

    if args.command == "new":
        manager.start_new_cycle(args.requirement_id)
    elif args.command == "approve":
        manager.approve()
    elif args.command == "set-stage":
        manager.set_stage(args.stage)

if __name__ == "__main__":
    main()
