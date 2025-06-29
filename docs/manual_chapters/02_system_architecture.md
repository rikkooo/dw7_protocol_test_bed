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
