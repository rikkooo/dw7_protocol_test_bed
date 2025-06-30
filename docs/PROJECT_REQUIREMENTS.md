# Master Requirements List

### ID: REQ-DW8-SYS-001

- **Title:** Implement Context Integrity Protocol

- **Description:** A critical vulnerability was identified where the AI can make incorrect assumptions about the purpose of core system files. This requirement implements a new protocol to protect the system's core by establishing rules for file interaction and context management.

- **SMRs:**
  - [ ] SMR-1: Update `docs/README.md` to include a new 'AI Operational Constraints' section, explicitly forbidding modification of core context files.
  - [ ] SMR-2: Create a permanent memory codifying the 'Principle of Evident Purpose' and the rule against modifying context files.
  - [ ] SMR-3: Verify the `README.md` file has been updated correctly.
  - [ ] SMR-4: Verify the permanent memory has been created successfully.
---
