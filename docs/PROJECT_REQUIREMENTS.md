# DW8 Protocol: Master Requirement Index

This document is the master list of all project requirements. It is a lightweight index that points to detailed requirement files.

Format: `[Status] [Priority] [ID] [Title] -> [Path]`

**Legend:**

- **Status:** `[P]` Pending, `[I]` In Progress, `[D]` Deployed, `[H]` Halted
- **Priority:** `[C]` Critical, `[H]` High, `[M]` Medium, `[L]` Low

---

[D] [C] [REQ-DW8-073] Architect and Implement a Pointer-Based Memory System -> ./reqs/REQ-DW8-073.md
[D] [C] [REQ-DW8-072] Simplify and Refine AI Context Refresh Protocol -> ./reqs/REQ-DW8-072.md
[D] [H] [REQ-DW8-074] End-to-End Test of New Architecture -> ./reqs/REQ-DW8-074.md
[D] [H] [REQ-DW8-001] Implement a persistent failure counter -> ./reqs/REQ-DW8-001.md
[D] [H] [REQ-DW8-002] Implement the Rehearsal State -> ./reqs/REQ-DW8-002.md
[D] [H] [REQ-DW8-004] Implement Rehearsal Stage Logic -> ./reqs/REQ-DW8-004.md
[D] [C] [REQ-DW8-011] Implement Deployer Configuration and Credential Management -> ./reqs/REQ-DW8-011.md
[D] [H] [REQ-DW8-008] Automate Standard Project Deployment -> ./reqs/REQ-DW8-008.md
[D] [H] [REQ-DW8-010] Implement Dual-Push for Protocol Evolution -> ./reqs/REQ-DW8-010.md

[D] [C] [REQ-DW8-075] Implement Robust Command Output Handling -> ./reqs/REQ-DW8-075.md
[D] [H] [REQ-DW8-013] Implement and Adhere to Dynamic Requirement Protocol -> ./reqs/REQ-DW8-013.md
[D] [M] [REQ-DW8-009] Generate Final Project Documentation -> ./reqs/REQ-DW8-009.md
[D] [M] [REQ-DW8-014] Implement Code Granularity Protocol to Improve Edit Reliability -> ./reqs/REQ-DW8-014.md
[P] [M] [REQ-DW8-019] Design a formal protocol for transitioning documentation from Markdown to a structured JSON format to improve machine readability and maintainability. -> ./reqs/REQ-DW8-019.md
[P] [H] [REQ-DW8-VAL-001] Perform a complete, end-to-end run of the DW8 workflow to validate the new engine. -> ./reqs/REQ-DW8-VAL-001.md
[D] [L] [REQ-DW8-012] Document Requirement List Abbreviations -> ./reqs/REQ-DW8-012.md

[D] [C] [REQ-DW8-OS-001] [Design] Formalize the "DW8 Operating System" architecture -> ./reqs/REQ-DW8-OS-001.md
[D] [C] [REQ-DW8-OS-002] [Execution] Replace `PROJECT_REQUIREMENTS.md` with Event Queues -> ./reqs/REQ-DW8-OS-002.md
[D] [C] [REQ-DW8-OS-003] [Execution] Create Migration Script for Existing Requirements -> ./reqs/REQ-DW8-OS-003.md
[D] [C] [REQ-DW8-OS-004] [Execution] Refactor Kernel to Read from `pending_events.json` -> ./reqs/REQ-DW8-OS-004.md
[D] [C] [REQ-DW8-OS-005] [Execution] Implement Event Queue Completion Logic -> ./reqs/REQ-DW8-OS-005.md
[D] [H] [REQ-DW8-OS-006] [Execution] Transition `workflow_state` to JSON -> ./reqs/REQ-DW8-OS-006.md
[D] [H] [REQ-DW8-OS-007] [Execution] Refactor Requirement Files to JSON Events -> ./reqs/REQ-DW8-OS-007.md
[P] [M] [REQ-DW8-OS-008] [Execution] Implement Decoupled Deployer Logic -> ./reqs/REQ-DW8-OS-008.md
[P] [M] [REQ-DW8-OS-009] [Execution] Implement Dynamic Event Prioritization -> ./reqs/REQ-DW8-OS-009.md
[P] [H] [REQ-DW8-OS-010] [Design] Design and Document a `BOOT_PROTOCOL.md` -> ./reqs/REQ-DW8-OS-010.md
[P] [M] [REQ-DW8-OS-011] [Design] Design and Document a `CONTEXT_MANAGEMENT_PROTOCOL.md` -> ./reqs/REQ-DW8-OS-011.md
[P] [H] [REQ-DW8-OS-012] [Design] Re-design the `Rehearsal` Stage as an Interrupt Handler -> ./reqs/REQ-DW8-OS-012.md

[D] [H] [REQ-DW8-015] [Sherlock Mode] Investigate and Redesign State Machine Gatekeeping Rules -> ./reqs/REQ-DW8-015.md
[P] [H] [REQ-DW8-016] [Sherlock Mode] Investigate and Fortify Workflow Adherence Protocol -> ./reqs/REQ-DW8-016.md
[P] [M] [REQ-DW8-017] [Execution] Refactor All Major Classes to Use Code Granularity Protocol -> ./reqs/REQ-DW8-017.md
[P] [H] [REQ-DW8-018] [Sherlock Mode] Investigate and Redesign Environment Management and Enforcement -> ./reqs/REQ-DW8-018.md
[P] [M] [REQ-DW8-019] [Sherlock Mode] Investigate and Enhance Git/Deployment Workflow -> ./reqs/REQ-DW8-019.md

[P] [C] [REQ-DW8-BUG-001] Fix Incorrect Command Invocation in Governor Rules -> ./reqs/REQ-DW8-BUG-001.md
[P] [C] [REQ-DW8-EXEC-001] [Execution] Refactor Governor for Centralized Gatekeeping -> ./reqs/REQ-DW8-EXEC-001.md
[P] [H] [REQ-DW8-EXEC-002] [Execution] Remove Decentralized Stage Validation Methods -> ./reqs/REQ-DW8-EXEC-002.md
[P] [H] [REQ-DW8-EXEC-003] [Execution] Deprecate and Remove 'allow_failures' Bypass -> ./reqs/REQ-DW8-EXEC-003.md
[P] [C] [REQ-DW8-EXEC-004] [Execution] Adapt WorkflowKernel for Governor-Led Transitions -> ./reqs/REQ-DW8-EXEC-004.md
[P] [M] [REQ-DW8-EXEC-005] [Execution] Implement Automatic Git Revert on Validation Failure -> ./reqs/REQ-DW8-EXEC-005.md
