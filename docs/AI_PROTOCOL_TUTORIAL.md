# AI Protocol Tutorial

This document is a quick-reference guide for the AI agent to refresh its understanding of the protocol's mechanics at the start of each work cycle.

---

## Core Workflow Stages

The DW8 protocol is a state machine designed to guide development in a structured and robust way. Each stage has a specific objective:

- **`Engineer`:** Define the problem, break it down into the smallest possible, verifiable sub-requirements (SMRs), and ensure the overall plan is sound. The output of this stage is a clear, actionable requirement in `docs/PROJECT_REQUIREMENTS.md`.

- **`Researcher`:** (Optional) If the solution is not obvious, this stage is used to explore different approaches, consult documentation, and create a detailed implementation plan. This prevents wasted effort in the Coder stage.

- **`Coder`:** Write the code to implement the specific SMRs for the current requirement. The focus is solely on implementation, not on design or planning.

- **`Validator`:** Run the automated test suite to ensure the new code works as expected and has not introduced any regressions. All tests must pass before advancing.

- **`Deployer`:** Deploys the changes. This stage has two critical responsibilities:
  - **Protocol Evolution:** If the `is_protocol_update` flag is set or if the workflow's source code has changed, this stage executes a special sub-workflow to version and release the new protocol.
  - **Protocol Synchronization:** After a successful protocol evolution, the `Deployer` automatically synchronizes the new kernel code. It copies the contents of `src/dw6` to the official `~/devs/dw/dw8` directory and pushes these changes to the `windsurf-development-workflow` repository. This ensures the master protocol is always current.

- **`Rehearsal`:** This is not a standard workflow stage but a special "time-out" state entered automatically after repeated failures in any other stage. Its purpose is to force a deep reflection on the failure. The AI must analyze the root cause, re-evaluate the plan, and propose at least two alternative solutions before being allowed to retry the failing stage.

---

## Key CLI Commands

The workflow is managed through a set of simple CLI commands:

- `uv run python -m dw6.main status`: Shows the current state of the workflow, including the current stage and requirement pointer.

- `uv run python -m dw6.main approve`: Approves the current stage's exit criteria and advances the workflow to the next stage.

- `uv run python -m dw6.main new`: Guides the user through creating a new requirement, which is then added to `docs/PROJECT_REQUIREMENTS.md`.

- `uv run python -m dw6.main meta-req`: A command to formalize a meta-level discussion (like a new protocol feature) into a structured requirement.

---

## Key Files

Three files are critical for maintaining the project's state and history:

- `.workflow_state`: A simple key-value file that stores the live state of the workflow. This includes the `CurrentStage`, `RequirementPointer`, `FailureCounters`, and, most importantly, the `PythonExecutablePath`. This path points to the correct Python executable within the project's virtual environment, ensuring all commands are run in the correct context.

- **`docs/PROJECT_REQUIREMENTS.md`**: This is now a lightweight **Master Requirement Index**. It contains only a prioritized list of pointers to detailed requirement files. Format: `[Status] [Priority] [ID] [Title] -> [Path]`.

- **`docs/reqs/`**: This directory contains the detailed files for each individual requirement (e.g., `REQ-DW8-073.md`). The `WorkflowKernel` reads the Master Index to find the active task and then loads the full context from the corresponding file in this directory.

---

## Failure Handling

The protocol is designed to be resilient and to handle failures gracefully:

- **Failure Counters:** The system tracks the number of consecutive failures for critical operations (e.g., running tests). If a counter exceeds a predefined threshold (e.g., 3), it indicates a persistent problem.

- **The Rehearsal State:** When a failure threshold is reached, the workflow automatically transitions to the `Rehearsal` state. This is a mandatory "time-out" where the AI must analyze the failure, re-read the requirements, and propose alternative solutions.

- **Escalation Protocol:** If the `Rehearsal` stage itself fails to produce a viable solution, the system automatically creates a new, `Critical` priority requirement to investigate the root cause. The workflow is then reset to the `Engineer` stage to force a re-evaluation of the problem, preventing the AI from getting stuck in a failure loop.
