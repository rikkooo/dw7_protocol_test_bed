# DW8 Operating System Architecture

This document outlines the formal architecture of the DW8 protocol, which is modeled after a lightweight, event-driven operating system. This paradigm provides a robust and extensible framework for managing complex, multi-stage development workflows.

## 1. Core Concepts

The DW8 OS is built upon several core concepts that mirror traditional operating systems:

- **Kernel:** The central orchestrator of the workflow.
- **Event Queue:** The sequence of requirements to be processed.
- **Registers:** The persistent state of the workflow.
- **Interrupts:** Mechanisms for handling exceptional events and altering the standard workflow.

## 2. Kernel

The `WorkflowKernel` is the heart of the DW8 OS. It is responsible for:

- Loading and interpreting the current requirement from the Event Queue.
- Managing stage transitions (e.g., from `Engineer` to `Coder`).
- Executing the logic associated with each stage.
- Interacting with the Registers to maintain state.

## 3. Event Queue

The Event Queue is a persistent, ordered list of tasks (requirements) to be executed. In DW8, this is implemented as a series of JSON files in the `events/` directory. The `RequirementPointer` register tracks the currently active event.

## 4. Registers

The Registers are the memory of the DW8 OS, holding all persistent state. This is implemented in the `data/workflow_state.json` file. Key registers include:

- `CurrentStage`: The current stage of the workflow.
- `RequirementPointer`: A pointer to the current event in the Event Queue.
- `is_protocol_update`: A flag to indicate if the current task is modifying the protocol itself.

## 5. Interrupt Handling

Interrupts are events that can alter the normal flow of the workflow. The DW8 OS will define a formal interrupt handling mechanism to manage events such as:

- **Protocol Update Interrupt:** Triggered when `is_protocol_update` is `true`, this will invoke a specialized sub-workflow to safely manage protocol changes.
- **Failure Interrupt:** Triggered when a stage fails repeatedly, this will halt the workflow and require manual intervention.
