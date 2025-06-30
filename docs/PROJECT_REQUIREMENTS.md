# Master Requirements List

### ID: REQ-DW8-DOC-003

- **Title:** [Prism Protocol] Consolidate Conceptual Documentation into Master Manifest

- **Description:** Create a single, canonical `docs/README.md` that serves as the project's master manifest. This file will absorb and replace the conceptual information currently scattered across `DW8_OPERATING_SYSTEM.md`, `AI_PROTOCOL_TUTORIAL.md`, and the individual protocol files.

- **SMRs:**
  - [ ] SMR-1: Read the content of all core protocol files from `docs/protocols/`.
  - [ ] SMR-2: Append the full, transcluded text of each protocol to the `docs/README.md` under a new 'Core Protocols' section.
  - [ ] SMR-3: Identify all old conceptual documents (`DW8_OPERATING_SYSTEM.md`, `AI_PROTOCOL_TUTORIAL.md`, etc.) for deletion.
  - [ ] SMR-4: Delete the identified old conceptual documents.
  - [ ] SMR-5: Verify that `docs/README.md` is correctly updated with the transcluded protocols and that the old documentation files have been removed.
---
