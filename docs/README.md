# DW8 Protocol: The Master Tool of Development

## 1. Vision and Mission

We are not just building an application. We are building the **Master Tool of Development**, a system that can manage an entire software development cycle, fully automatized. It's a factory for creating pristine, robust software.

Our mission is to create a self-aware, resilient development framework that can combat cognitive fixation, prevent context decay, and enforce robust operational protocols. The DW8 protocol is an evolution, designed to create a more intelligent and autonomous development process.

## 2. System Architecture

The DW8 system is architected as a state machine managed by a central **Governor** and **AI Kernel**.

- **The Governor:** The master controller of the workflow. It is responsible for all state transitions, ensuring they are logical and follow protocol.
- **The AI Kernel:** The 'brain' of the operation, responsible for executing the tasks within each stage of the workflow.
- **The State Manager:** The system's memory. It is a passive component that records the state of the workflow in a JSON file (`data/workflow_state.json`). The State Manager only records the state; the Governor dictates it.

The workflow progresses through a series of well-defined stages:

- **`Engineer` -> `Researcher` -> `Coder` -> `Validator` -> `Deployer`:** The primary path from high-level planning to a deployed solution.
- **`Rehearsal` (Circuit Breaker):** A special, reflective state triggered by repeated failures in any other stage.
- **`Sherlock Mode` (Investigation):** A designated phase for deep investigation and design *before* any code is written.
- **`Execution Mode` (Implementation):** The phase for writing code to implement a previously designed solution.

## 3. Key Protocols

The DW8 system operates on a set of formal, documented procedures that govern how specific, critical tasks are performed.

- **Living Documentation Protocol:** Ensures that all code changes are accompanied by corresponding documentation updates.
- **Robust Command Protocol:** A procedure for capturing the full, untruncated output of critical shell commands to ensure accurate analysis.
- **Dynamic Requirement Protocol:** A system for managing a master list of prioritized requirements.
- **Deployment Protocol:** A formal process for versioning and releasing new versions of the DW protocol itself.

## 4. Operational Commands

The primary interface for the human Principal is the command-line interface (CLI), `dw6_cli.py`.

- **`dw6 new <requirement_id> ...`**: Initiates a new work session for a specific requirement.
- **`dw6 approve`**: Approves the completion of the current workflow stage and advances to the next.
- **`dw6 status`**: Displays the current state of the system.

For detailed usage, please refer to the `RECOVERY_PROTOCOL_VERBOSE.md` document in the `context` directory.

## 5. AI Operational Constraints

- **Principle of Evident Purpose:** The AI must not modify or delete any file that appears to be part of the system's context or configuration without first verifying its role. To do this, the AI must use `grep` to determine who reads from and writes to the file.
- **Context Immutability:** Core context files, including this `README.md`, are considered read-only unless a specific requirement explicitly directs their modification. Their purpose is to provide static context, not to be a deliverable.
