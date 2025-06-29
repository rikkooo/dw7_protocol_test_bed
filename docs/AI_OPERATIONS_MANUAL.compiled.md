# Chapter: 01 Vision And Mission



---

# Chapter 1: Vision and Mission

## 1.1. Core Mission

The DW8 Protocol is a next-generation framework designed to facilitate a highly collaborative and efficient partnership between a human developer (the 'Principal') and a sophisticated AI agent (the 'Gem'). Its primary goal is to create a structured, predictable, and robust environment where the AI can function as a true pair programmer, capable of complex, multi-step tasks with minimal cognitive overhead for the human.

## 1.2. Guiding Principles

1.  **Clarity over Cleverness:** The system's internal logic, state transitions, and protocols must be explicit, simple, and easily understood by both human and AI. Ambiguity is the enemy.
2.  **Trust through Verification:** The AI's autonomy is earned through a system of rigorous, automated checks and balances. The Governor acts as the unblinking eye, ensuring every action aligns with the established protocols.
3.  **Structured Freedom:** The AI operates within a well-defined set of rules and workflows. This structure is not a cage; it is a scaffold that enables the AI to perform complex tasks confidently and safely.
4.  **Sustainable Cognition:** The documentation and context-refreshment systems are designed to combat AI context decay, ensuring the AI's understanding of the project remains complete and up-to-date over long periods.

## 1.3. The End State

The desired end state is a development workflow where the Principal can express intent at a high level (e.g., "Implement feature X as outlined in this design document"), and the Gem can execute the entire lifecycle of that task—from coding and testing to documentation and deployment—with minimal intermediate supervision.


---

# Chapter: 02 System Architecture



---

# Chapter 2: System Architecture

## 2.1. Overview

The DW8 Protocol is built on a modular architecture designed to separate concerns and create clear lines of responsibility. The system is composed of several key components that work in concert to manage the development workflow.

## 2.2. Core Components

1.  **The AI Kernel (`dw6/kernel.py`):** This is the heart of the AI's reasoning and execution capabilities. It is responsible for receiving instructions, invoking tools, and generating responses. It is the engine.

2.  **The Governor (`dw6/governor.py`):** The Governor is the master controller and protocol enforcer. It sits above the Kernel and orchestrates the entire workflow. It manages the state machine, validates AI actions against protocol rules, and serves as the ultimate gatekeeper for all significant operations. It is the brain.

3.  **The State Manager (`dw6/state_manager.py`):** This component is the single source of truth for the project's state. It tracks the current stage of the workflow (e.g., Engineer, Coder, Deployer), manages the backlog of requirements, and persists the system's state between sessions. It is the memory.

4.  **Workflow Stages (`dw6/workflow/`):** The workflow is broken down into discrete stages, each with a specific purpose and set of allowed actions. These stages are implemented as Python modules and are invoked by the Governor based on the current state.

5.  **Command-Line Interface (`dw6_cli.py`):** This is the primary entry point for the human Principal to interact with the system. It provides commands to initiate workflows, approve stages, and manage requirements.

## 2.3. Data Flow

- The **Principal** issues a command via the **CLI**.
- The **CLI** invokes a method on the **Governor**.
- The **Governor** consults the **State Manager** to understand the current context.
- The **Governor** invokes the appropriate **Workflow Stage** and passes control to the **AI Kernel** with a specific prompt and set of constraints.
- The **AI Kernel** performs its task, potentially using tools that interact with the file system or other resources.
- The **Governor** validates the result and, if successful, updates the **State Manager** to reflect the new state of the system.


---

# Chapter: 03 Key Protocols



---

# Chapter 3: Key Protocols

## 3.1. The State Machine Protocol

The entire workflow is governed by a strict, explicit state machine. The system can only be in one of the following states at any given time:

- **IDLE:** The system is waiting for a command.
- **ENGINEER:** The AI is in a planning and design phase. Code modification is forbidden.
- **CODER:** The AI is in the implementation phase. Code modification is permitted.
- **VALIDATOR:** The AI is in a testing and validation phase.
- **DEPLOYER:** The AI is preparing the code for release and performing final checks.

The Governor is responsible for all state transitions. Transitions are only allowed in a predefined sequence (e.g., Coder -> Validator -> Deployer). Any attempt to perform an action not allowed in the current state will be rejected.

## 3.2. The AI-Cognitive Documentation Framework (AI-CDF)

This is the master protocol for managing the AI's long-term memory and context. It is composed of three pillars:

1.  **Dynamic Mission Briefs (`_CONTEXT.md`):** Provide immediate, just-in-time context for specific tasks.
2.  **The Composable Operations Manual:** Provides a mechanism for total project recall through a buildable, comprehensive manual.
3.  **The 'Smart' Living Documentation Protocol:** Enforces that documentation is updated as a mandatory part of the development lifecycle.

## 3.3. The 'Smart' Living Documentation Protocol

This protocol ensures that the Operations Manual never becomes stale. It is a hard gate in the `Deployer` stage.

- **Mechanism:** Before a deployment can be approved, the Governor checks if a `_CONTEXT.md` file was modified. If so, it finds the linked master chapter via metadata (`Manual-Chapter: ...`) and asks the AI to confirm that the corresponding chapter has also been updated.
- **Purpose:** This creates a direct, low-cost, and enforceable link between code changes and documentation updates, ensuring the long-term health of the project's knowledge base.


---

# Chapter: 04 Governor And Ai Kernel



---

# Chapter 4: The Governor and AI Kernel

## 4.1. The Governor: The Master Controller

The Governor (`dw6/governor.py`) is the central authority of the DW8 system. It is not the AI; it is the master process that directs the AI. Its responsibilities are absolute.

- **State Machine Management:** The Governor owns the state machine. It initiates all stage transitions and is the sole source of truth for the system's current state (`ENGINEER`, `CODER`, etc.).

- **Protocol Enforcement:** The Governor enforces all system protocols. It checks every proposed action from the AI against the rules of the current stage. For example, it will block any attempt to write code during the `ENGINEER` stage.

- **Prompt Orchestration:** The Governor is responsible for constructing the precise prompts and instructions given to the AI Kernel. This includes prepending dynamic context from `_CONTEXT.md` files.

- **Validation and Gating:** The Governor acts as the final gatekeeper for all major workflow transitions. It runs validation checks, such as the Living Documentation Protocol, before allowing a stage to be marked as complete.

## 4.2. The AI Kernel: The Engine of Creation

The AI Kernel (`dw6/kernel.py`) is the interface to the Large Language Model (LLM). It is a powerful but subordinate component, always acting under the direction of the Governor.

- **Instruction Execution:** The Kernel's primary job is to receive a prompt from the Governor and execute it. This involves reasoning, planning, and using the available tools (e.g., `write_to_file`, `run_command`).

- **Tool Usage:** The Kernel has access to a suite of tools to interact with the environment. All tool usage is subject to the Governor's validation.

- **Response Generation:** The Kernel generates the text-based responses, code, and other artifacts requested by the Governor's prompt.

## 4.3. The Relationship: Brain and Hands

- The **Governor** is the **brain**. It decides *what* to do, *when* to do it, and *why*. It is strategic, deliberate, and focused on maintaining order and following protocol.
- The **AI Kernel** is the **hands**. It figures out *how* to do what the Governor has commanded. It is tactical, creative, and focused on executing the immediate task.

This separation is the most critical architectural decision in the DW8 protocol. It allows the system to be both highly intelligent and extremely reliable.


---

# Chapter: 05 State Manager



---

# Chapter 5: The State Manager

## 5.1. Role and Purpose

The State Manager (`dw6/state_manager.py`) is the definitive source of truth for the project's operational state. Its sole purpose is to load, manage, and persist the system's status to disk, ensuring that context is never lost between sessions.

It is the system's memory.

## 5.2. The State File

The State Manager's data is persisted in a single JSON file: `.dw6_state.json`.

This file is the canonical record of:

- **Current Workflow Stage:** The active stage of the state machine (e.g., `ENGINEER`, `CODER`).
- **Active Requirement:** The ID of the requirement currently being worked on.
- **Requirement Backlog:** A list of all known requirements and their current status (e.g., `pending`, `in_progress`, `completed`).
- **Session History:** A log of major events and stage transitions.

## 5.3. Key Operations

The State Manager provides a simple, clear API for the Governor to use:

- `load_state()`: Reads `.dw6_state.json` from disk and loads it into memory at the beginning of a session.
- `save_state()`: Writes the current in-memory state back to `.dw6_state.json`. The Governor calls this method after every significant change (e.g., completing a stage, adding a requirement).
- `get_current_stage()`: Returns the active workflow stage.
- `update_stage(new_stage)`: Sets the new active workflow stage.
- `get_requirement(req_id)`: Retrieves the details of a specific requirement.
- `add_requirement(requirement)`: Adds a new requirement to the backlog.

## 5.4. Integrity

The State Manager is designed for simplicity and robustness. It performs basic validation to ensure the integrity of the state file but relies on the Governor to ensure that all state transitions are logical and follow protocol. The State Manager only records the state; the Governor dictates it.


---

# Chapter: 06 Operational Commands



---

# Chapter 6: Operational Commands

## 6.1. Overview

The primary interface for the human Principal is the command-line interface (CLI), `dw6_cli.py`. These commands are the triggers for all major workflow actions.

## 6.2. Core Commands

### `dw6-dev-sec.py start <requirement_id>`

- **Purpose:** Initiates a new work session for a specific requirement.
- **Action:** The Governor loads the system state, sets the specified requirement as active, and transitions the state machine to the first stage (typically `ENGINEER`). It then provides the AI Kernel with its initial instructions.
- **Example:** `uv run python dw6_cli.py start REQ-DW8-EXEC-001`

### `dw6-dev-sec.py approve`

- **Purpose:** To approve the completion of the current workflow stage and advance to the next.
- **Action:** The Principal uses this command after reviewing the AI's work in the current stage. The Governor performs any necessary validation for the current stage (e.g., the Living Documentation Protocol check in the `DEPLOYER` stage). If validation passes, the Governor transitions the state machine to the next stage and saves the new state.
- **Example:** `uv run python dw6_cli.py approve`

### `dw6-dev-sec.py add-req <path_to_json>`

- **Purpose:** Adds a new requirement to the project backlog.
- **Action:** The State Manager reads the requirement definition from the specified JSON file and adds it to the list of pending requirements in the state file.
- **Example:** `uv run python dw6_cli.py add-req events/REQ-DW8-DOC-010.json`

### `dw6-dev-sec.py status`

- **Purpose:** Displays the current state of the system.
- **Action:** The State Manager reads the state file and prints a summary of the current stage, the active requirement, and the status of the requirement backlog.
- **Example:** `uv run python dw6_cli.py status`
