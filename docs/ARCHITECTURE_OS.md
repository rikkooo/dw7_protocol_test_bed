# DW8 Operating System Architecture

## 1. Overview

This document outlines the architecture of the DW8 protocol, reframed as a bespoke, lightweight Operating System (OS). This paradigm provides a robust and scalable model for managing development workflows, treating requirements as "events," stages as "instruction sets," and the core logic as a "kernel."

## 2. Core Components

### 2.1. The Kernel (`WorkflowManager`)

The `WorkflowManager` is the central Kernel of the OS. Its responsibilities include:

- **Process Scheduling:** Fetching the next event from the `pending_events.json` queue.
- **Instruction Execution:** Invoking the correct instruction set (workflow stages) based on the event's type.
- **State Management:** Interacting with the Registers (`workflow_state.json`) to track system state.
- **Interrupt Handling:** Managing failures and invoking the `Rehearsal` state (Interrupt Handler).

### 2.2. Event Queues

The system uses two primary queues to manage the flow of work:

- **`pending_events.json`:** A FIFO queue of tasks to be processed. Each entry is a lightweight pointer to a full event definition. High-priority events can be injected at the front of the queue, acting as interrupts.
- **`processed_events.json`:** An immutable log of completed events, serving as a historical record of all work done.

### 2.3. Events & Instruction Sets

- **Event:** A requirement or task, defined in a JSON file within the `/events/` directory. An event contains metadata (ID, priority, title) and defines the sequence of instructions needed to complete it.
- **Instruction Set:** A workflow stage (e.g., `Engineer`, `Coder`, `Validator`). These are the atomic operations the Kernel can execute on an event.

### 2.4. Registers (`workflow_state.json`)

A simple, volatile JSON file that holds the current state of the "CPU." It contains only the most essential, frequently changing data:

- `current_event_pointer`: The ID of the event being processed.
- `current_stage`: The instruction currently being executed.
- `system_flags`: Critical booleans like `is_protocol_update`.

### 2.5. Interrupt Handler (`Rehearsal` Stage)

The `Rehearsal` stage functions as the system's primary Interrupt Handler. It is triggered by the Kernel after repeated failures of a specific instruction. Its job is to pause the event, analyze the failure, formulate a new plan, and then re-queue the event for processing.

## 3. Workflow Lifecycle (Boot to Shutdown)

1. **Boot Sequence:** A defined `BOOT_PROTOCOL` initializes the environment, loads the Kernel, and prepares the event queues.
2. **Event Loop:** The Kernel enters its main loop:
    a. Fetch the next event from the pending queue.
    b. Load the event's instruction set.
    c. Execute instructions sequentially (`Engineer` -> `Coder`...).
    d. On success, move the event to the processed queue.
    e. On failure, trigger the Interrupt Handler.
3. **Context Management:** Periodically, the Kernel will refresh the AI's context to prevent decay, guided by the `CONTEXT_MANAGEMENT_PROTOCOL`.
