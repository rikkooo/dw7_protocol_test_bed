# DW8 System Architecture

## 1. Project Purpose & Core Philosophy

This project, the Development Workflow 8 (DW8) Protocol, is a meta-platform designed to create a structured, self-correcting environment for AI-driven software development. Its primary purpose is to transform an AI agent from a simple tool into a reliable, autonomous engineering partner.

We are building this system to solve two fundamental challenges in AI-assisted development:

1.  **Cognitive Fixation:** The tendency for an AI to get stuck in a repetitive loop, retrying a failing approach without the self-awareness to adapt. The DW8 protocol counters this with its **Rehearsal State** and **Escalation Protocol**.

2.  **Context Decay:** The tendency for an AI's limited context window to cause it to forget high-level goals and strategic decisions over time. The DW8 protocol fights this with a **master requirements file** and a **mandatory context refresh protocol**.

The ultimate vision is a system where a human developer can confidently delegate a complex software development goal to an AI, trusting the DW8 protocol to guide the AI to execute the task intelligently and resiliently.

## 2. State Machine Diagram

The DW8 protocol operates as a state machine. The primary goal is to move a requirement from `Pending` to `Deployed` by successfully passing through each stage. The system is designed to be resilient, with a built-in mechanism for handling persistent failures.

```

[ START: Read Master Requirement Index ]
    |
    | (Select Highest Priority Pending Requirement)
    v
+----------+
| Engineer |
+----------+
    |
    | (Needs Research?)
    +--------------------[Yes]------------------->+------------+
    |                                            | Researcher |
    |                                            +------------+
    |                                                 |
    v                                                 v
+-------+                                       +-----------+
| Coder |<--------------------------------------+           |
+-------+
    |
    | [Success]
    v
+-----------+
| Validator |
+-----------+
    |
    | [Success]
    v
+----------+
| Deployer |
+----------+
    |
    | [Cycle Complete]
    +---------------------------------------------> [ START ]


FAILURE & ESCALATION PATH (Applies to Coder, Validator, Deployer stages)

(From a Failing Stage)
    |
    | [On Failure]
    v
+-------------------------+
|  Increment Failure      |
|  Counter for Operation  |
+-------------------------+
    |
    | (Count < Failure Threshold?)
    +--------------------[Yes]-------------------> [ Retry Stage ]
    |
    | (Count >= Failure Threshold?)
    v
+------------------------------------+
|       Escalation Protocol          |
| - Create new 'Critical' Red Flag   |
|   Requirement for this failure.    |
| - Reset workflow to Engineer stage.|
+------------------------------------+
    |
    v
[ START ]

```

## 3. Core Components

The DW8 system is composed of several key classes, each with a distinct responsibility. They work together to create a robust and managed development process.

- **`WorkflowManager` (`state_manager.py`):** The central orchestrator of the entire system. It is responsible for loading the current stage, invoking the stage's validation logic upon an `approve` command, and advancing the workflow to the next stage. It holds instances of the `Governor` and `WorkflowKernel`.

- **`WorkflowKernel` (`kernel.py`):** The engine of the workflow. It handles the core logic of state transitions, such as advancing the stage, saving commit SHAs, and, most importantly, executing the failure handling protocol (the Escalation Protocol) when a stage fails repeatedly.

- **`Governor` (`state_manager.py`):** The security layer. It maintains a strict set of rules defining which commands are authorized in each stage of the workflow. Before any command is executed, the Governor checks if it is permitted, preventing unauthorized actions.

- **`WorkflowState` (`state_manager.py`):** The persistence layer. This class is responsible for reading, writing, and managing the `.workflow_state` file. It handles creating the virtual environment and storing critical state information like the `CurrentStage`, `RequirementPointer`, `FailureCounters`, and the all-important `PythonExecutablePath`.

- **Stage Classes (`engineer.py`, `coder.py`, etc.):** Each stage of the workflow (Engineer, Coder, Validator, Deployer) is encapsulated in its own class. These classes contain the specific logic and validation criteria for that particular stage. For example, the `ValidatorStage` is responsible for running `pytest`, while the `DeployerStage` handles the Protocol Evolution sub-workflow.

## 4. Folder Structure

The project is organized into several key directories to separate concerns and maintain clarity.

- **`.venv/`**: The project's virtual environment, automatically created and managed by `WorkflowState`. It contains all the necessary Python dependencies, ensuring a consistent and isolated development environment.

- **`docs/`**: Contains all project-related documentation.
  - **`ARCHITECTURE.md`**: This file. The single source of truth for the project's design and structure.
  - **`PROJECT_REQUIREMENTS.md`**: The master list of all tasks and their statuses. (This will be re-architected into a lightweight index as per REQ-DW8-073).
  - **`AI_PROTOCOL_TUTORIAL.md`**: A concise guide for the AI agent to refresh its understanding of the workflow.

- **`src/dw6/`**: The core source code of the DW8 protocol.
  - **`workflow/`**: Contains the individual Python modules for each stage (`engineer.py`, `coder.py`, etc.).
  - **`main.py`**: The entry point for the command-line interface (CLI), handling commands like `approve` and `status`.
  - **`state_manager.py`**: Contains the `WorkflowManager`, `Governor`, and `WorkflowState` classes.
  - **`kernel.py`**: Contains the `WorkflowKernel` class, which handles the core state transition and failure logic.

- **`tests/`**: Contains all the automated tests for the project, which are run by the `Validator` stage.

- **`.workflow_state`**: A critical file in the root directory that persists the live state of the workflow between commands and sessions.
