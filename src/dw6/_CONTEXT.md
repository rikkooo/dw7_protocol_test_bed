# CONTEXT: DW6 Protocol Core

*** GEM, READ THIS! *** This directory contains the core logic for the DW6/DW8 protocol.

## Purpose

This module is the heart of the system, containing the Governor, the AI Kernel, the State Manager, and the workflow stage definitions. It orchestrates the entire development process, from requirement intake to deployment.

## Key Components

-   `governor.py`: The master controller and protocol enforcer. **All major workflow logic originates here.**
-   `kernel.py`: The interface to the LLM. It executes commands from the Governor.
-   `state_manager.py`: Manages the `.dw6_state.json` file, the single source of truth for the system's state.
-   `workflow/`: This subdirectory contains the implementation for each specific stage of our state machine (Engineer, Coder, etc.).

## Manual Chapter Link

-   **Manual-Chapter:** `02_system_architecture.md`
