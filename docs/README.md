# DW8 Protocol: The Master Tool of Development

## Chapter 1: Vision and Mission

### 1.1. Core Mission

The DW8 Protocol is a next-generation framework designed to facilitate a highly collaborative and efficient partnership between a human developer (the 'Principal') and a sophisticated AI agent (the 'Gem'). Its primary goal is to create a structured, predictable, and robust environment where the AI can function as a true pair programmer, capable of complex, multi-step tasks with minimal cognitive overhead for the human.

### 1.2. Guiding Principles

1.  **Clarity over Cleverness:** The system's internal logic, state transitions, and protocols must be explicit, simple, and easily understood by both human and AI. Ambiguity is the enemy.
2.  **Trust through Verification:** The AI's autonomy is earned through a system of rigorous, automated checks and balances. The Governor acts as the unblinking eye, ensuring every action aligns with the established protocols.
3.  **Structured Freedom:** The AI operates within a well-defined set of rules and workflows. This structure is not a cage; it is a scaffold that enables the AI to perform complex tasks confidently and safely.
4.  **Sustainable Cognition:** The documentation and context-refreshment systems are designed to combat AI context decay, ensuring the AI's understanding of the project remains complete and up-to-date over long periods.

### 1.3. The End State

The desired end state is a development workflow where the Principal can express intent at a high level (e.g., "Implement feature X as outlined in this design document"), and the Gem can execute the entire lifecycle of that task—from coding and testing to documentation and deployment—with minimal intermediate supervision.

## Chapter 2: System Architecture

The DW8 Protocol is built on a modular architecture designed to separate concerns and create clear lines of responsibility. The core components are the Governor, the AI Kernel, and the State Manager.

## Chapter 3: Key Protocols

### 3.1. The State Machine Protocol

The entire workflow is governed by a strict, explicit state machine. The system can only be in one of the following states at any given time:

- **IDLE:** The system is waiting for a command.
- **ENGINEER:** The AI is in a planning and design phase. Code modification is forbidden.
- **CODER:** The AI is in the implementation phase. Code modification is permitted.
- **VALIDATOR:** The AI is in a testing and validation phase.
- **DEPLOYER:** The AI is preparing the code for release and performing final checks.

The Governor is responsible for all state transitions. Transitions are only allowed in a predefined sequence (e.g., Coder -> Validator -> Deployer). Any attempt to perform an action not allowed in the current state will be rejected.

### 3.2. The AI-Cognitive Documentation Framework (AI-CDF)

This is the master protocol for managing the AI's long-term memory and context. It is composed of three pillars:

1.  **Dynamic Mission Briefs (`_CONTEXT.md`):** Provide immediate, just-in-time context for specific tasks.
2.  **The Composable Operations Manual:** Provides a mechanism for total project recall through a buildable, comprehensive manual.
3.  **The 'Smart' Living Documentation Protocol:** Enforces that documentation is updated as a mandatory part of the development lifecycle.

### 3.3. The 'Smart' Living Documentation Protocol

This protocol ensures that the Operations Manual never becomes stale. It is a hard gate in the `Deployer` stage.

- **Mechanism:** Before a deployment can be approved, the Governor checks if a `_CONTEXT.md` file was modified. If so, it finds the linked master chapter via metadata (`Manual-Chapter: ...`) and asks the AI to confirm that the corresponding chapter has also been updated.
- **Purpose:** This creates a direct, low-cost, and enforceable link between code changes and documentation updates, ensuring the long-term health of the project's knowledge base.

## Chapter 4: Governor and AI Kernel

The Governor is the master controller of the workflow. It is responsible for all state transitions, ensuring they are logical and follow protocol. The AI Kernel is the 'brain' of the operation, responsible for executing the tasks within each stage of the workflow.

## Chapter 5: State Manager

The State Manager is the system's memory. It is a passive component that records the state of the workflow in a JSON file (`data/workflow_state.json`). The State Manager only records the state; the Governor dictates it.

## Chapter 6: Operational Commands

### 6.1. Overview

The primary interface for the human Principal is the command-line interface (CLI), `dw6_cli.py`. These commands are the triggers for all major workflow actions.

### 6.2. Core Commands

#### `dw6-dev-sec.py start <requirement_id>`

- **Purpose:** Initiates a new work session for a specific requirement.
- **Action:** The Governor loads the system state, sets the specified requirement as active, and transitions the state machine to the first stage (typically `ENGINEER`). It then provides the AI Kernel with its initial instructions.
- **Example:** `uv run python dw6_cli.py start REQ-DW8-EXEC-001`

#### `dw6-dev-sec.py approve`

- **Purpose:** To approve the completion of the current workflow stage and advance to the next.
- **Action:** The Principal uses this command after reviewing the AI's work in the current stage. The Governor performs any necessary validation for the current stage (e.g., the Living Documentation Protocol check in the `DEPLOYER` stage). If validation passes, the Governor transitions the state machine to the next stage and saves the new state.
- **Example:** `uv run python dw6_cli.py approve`

#### `dw6-dev-sec.py add-req <path_to_json>`

- **Purpose:** Adds a new requirement to the project backlog.
- **Action:** The State Manager reads the requirement definition from the specified JSON file and adds it to the list of pending requirements in the state file.
- **Example:** `uv run python dw6_cli.py add-req events/REQ-DW8-DOC-010.json`

#### `dw6-dev-sec.py status`

- **Purpose:** Displays the current state of the system.
- **Action:** The State Manager reads the state file and prints a summary of the current stage, the active requirement, and the status of the requirement backlog.
- **Example:** `uv run python dw6_cli.py status`

## AI Operational Constraints

- **Principle of Evident Purpose:** The AI must not modify or delete any file that appears to be part of the system's context or configuration without first verifying its role. To do this, the AI must use `grep` to determine who reads from and writes to the file.
- **Context Immutability:** Core context files, including this `README.md`, are considered read-only unless a specific requirement explicitly directs their modification. Their purpose is to provide static context, not to be a deliverable.
