### ID: REQ-DW8-073

- **Title:** Architect and Implement a Pointer-Based Memory System
- **Status:** `Pending`
- **Priority:** `Critical`
- **Details:** Re-architect the project's memory and requirement management from a single monolithic file to a granular, pointer-based system. This will drastically reduce the AI's working context, improve focus, and solve context decay.
- **SMRs:**
  - [ ] **SMR-DW8-073.1:** Establish the new directory structure for individual requirement files (e.g., `docs/reqs/`).
  - [ ] **SMR-DW8-073.2:** Redefine `docs/PROJECT_REQUIREMENTS.md` to be a lightweight 'Master Requirement Index' with the format `[Markers] [Title] -> [Path]`.
  - [ ] **SMR-DW8-073.3:** Implement the logic for creating and managing individual requirement and bug-report files in their respective directories.
  - [ ] **SMR-DW8-073.4:** Update the `WorkflowManager` to follow the new 'read index -> read specific file' workflow.
  - [ ] **SMR-DW8-073.5:** Create a migration script to convert existing requirements into the new granular format.
  - [ ] **SMR-DW8-073.6:** Update the `AI_PROTOCOL_TUTORIAL.md` to reflect this new, more efficient way of working.