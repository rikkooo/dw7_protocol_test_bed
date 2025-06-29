# The DW8 Master Guide: A Document to Rule Them All

**Version:** 1.0
**Purpose:** This document is the definitive, canonical source of truth for any agent or human seeking to understand and operate within the DW8 autonomous software development framework. It is designed to be verbose and deeply explanatory to eliminate ambiguity and prevent context loss.

---

## 1. The Windsurf Workflow: The True Entry Point

**This is the most critical architectural concept to understand.** This project does not exist in a vacuum. It operates as a **Windsurf Workflow**. The entire lifecycle of the project, from creation to daily operation, is initiated by user commands in the Windsurf interface.

* **The Starting Scripts:** The true entry points to this system are the Markdown files located in `/home/ubuntu/devs/.windsurf/workflows/`. Specifically, the script at `/home/ubuntu/devs/.windsurf/workflows/start-project-dw8.md` is responsible for setting up a new project instance.
* **Implication for Boot Process:** Any changes to the system's boot or environment setup **must** be compatible with this starting script. The script defines the user's first interaction with the system, and its instructions must remain valid. Before modifying any boot-related code, you must first consult the relevant start script to ensure your changes will not break the user-facing workflow.

---

## 2. The Vision: What Are We Building?

The DW8 project is not about building a single application. It is about building the **factory** that builds applications. We are creating a **meta-system for autonomous software development**, a platform where a human operator can provide high-level strategic direction, and an AI agent can execute the entire software development lifecycle with minimal intervention.

**The Core Problem:** Traditional software development is slow, expensive, and prone to human error. AI agents, while powerful, can suffer from cognitive fixation and context decay, leading them to get stuck in unproductive loops or lose sight of the project's goals.

**The DW8 Solution:** This platform solves these problems by creating a highly structured, protocol-driven environment. It provides the scaffolding for an AI agent to work reliably and autonomously, turning high-level requirements into robust, production-ready code.

---

## 3. The Architecture: A Protocol-Driven State Machine

The system is a modular, dynamically loaded state machine governed by a set of explicit protocols. This design emphasizes flexibility, predictability, and robustness.

**Architectural Diagram:**

```mermaid
graph TD
    A[User Command] --> B{dw6 cli.py};
    B --> C[WorkflowManager];
    C --> D{WorkflowKernel};
    C <--> E[WorkflowState];
    E <--> F[(data/workflow_state.json)];
    D --> G{Kernel Methods (kr/*.py)};
    C --> H{Manager Methods (st/*.py)};
    D <--> I[(events/*.json)];

    subgraph Core
        C
        D
        E
    end

    subgraph Data
        F
        I
    end

    subgraph Dynamic Code
        G
        H
    end
```

**Key Components:**

* **`dw6` (CLI Entry Point):** The system's entry point, parsing user commands (`status`, `approve`, etc.) and initializing the core components.
* **`WorkflowState`:** The system's memory. It loads and manages the live state from `data/workflow_state.json`, tracking the current stage, active requirement, and failure counters.
* **`WorkflowManager`:** The high-level orchestrator. It is a lean class that dynamically loads its methods from the `st/` (State) directory. It is responsible for transitioning between workflow stages (`Engineer`, `Coder`, etc.).
* **`WorkflowKernel`:** The engine that does the work. It also loads its methods dynamically, from the `kr/` (Kernel) directory. It executes the core logic for each stage, such as reading files, writing code, and running tests.

---

## 4. The Rulebook: The DW8 Protocols

The `docs/protocols/` directory is the most important part of this project. It contains the formal, explicit rules that govern the AI's behavior. Understanding these protocols is essential to understanding the system.

* **`BOOT_PROTOCOL.md`:** Defines the strict, sequential process for system startup, ensuring a consistent and reliable initialization every time.
* **`CONTEXT_MANAGEMENT_PROTOCOL.md`:** Outlines the procedures for how the AI should manage and recover its own context to prevent amnesia.
* **`DW8_CODE_GRANULARITY_PROTOCOL.md`:** Enforces a modular architecture by requiring that large classes be broken down into smaller, dynamically loaded methods.
* **`DW8_DEPLOYER_PROTOCOL.md`:** A formal process for versioning and releasing new versions of the DW8 protocol itself, treating the framework like a real software product.

---

## 5. The Data: Source of Truth

* **`events/` (Directory):** This is the **single source of truth for all project requirements**. Each task the system works on is defined by a JSON file in this directory. This is the system's backlog and to-do list.
* **`data/workflow_state.json` (File):** This is the live, operational state of the system. It is a simple file that tracks the `CurrentStage` and the `RequirementPointer` (the ID of the requirement currently being worked on). It is managed automatically by the `WorkflowState` class and should not be edited manually.

---

## 6. Core Documentation & Historical Context

The `docs/` directory contains key documents that provide architectural overviews, tutorials, and historical context. While the protocols are the active rules, these documents offer the 'why' behind the design.

* **`DW8_OPERATING_SYSTEM.md` (Core Architecture):** This is the definitive document that describes the architecture of the DW8 Operating System itself. It details the philosophy of the dynamic, modular kernel and manager, which is central to the system's flexibility.
* **`ARCHITECTURE_OS.md` (Deprecated):** This file's content has been moved to `DW8_OPERATING_SYSTEM.md`. This file is now deprecated and will be removed in a future update.
* **`AI_PROTOCOL_TUTORIAL.md` (Core Concept):** A quick-reference guide for an AI agent, summarizing the purpose of each workflow stage (`Engineer`, `Coder`, `Validator`, etc.) and the critical `Rehearsal` state for overcoming failures.
* **`PROJECT_SUMMARY.md` (Current State):** Provides a snapshot of the project's status at the beginning of the DW8 development epic. It clarifies that the initial work is focused on "Sherlock Mode"—investigating and designing the core protocols before implementation.
* **`PROJECT_REQUIREMENTS.md` (Legacy):** This was the original, Markdown-based system for tracking requirements. It has been **superseded by the JSON-based system in the `events/` directory**. It is preserved for historical reference.
* **`ARCHITECTURE.md` (Legacy):** Describes the architecture of a previous version of the system (DW7). It is useful for understanding the project's lineage but does not reflect the current DW8 architecture.
* **`WORKFLOW_MASTER.md` & `DW6_ISSUES.md` (Historical):** These documents provide context on the DW6 protocol, the predecessor to this system. They chronicle its completion and the issues that led to the development of the more robust DW8 framework.

---

## 7. How to Operate This System

1. **Define a Requirement:** Create a new JSON file in the `events/` directory that describes the task to be completed.
2. **Set the Pointer:** Update the `RequirementPointer` in `data/workflow_state.json` to point to the ID of your new requirement.
3. **Run the System:** Execute the main entry point (`dw6`) with a command like `status` to begin the workflow.
4. **Observe and Approve:** The AI will now follow the protocols to execute the requirement. It will propose actions (like file edits or commands) that you will need to approve. The system is designed to be a partnership between the human operator and the AI agent.
