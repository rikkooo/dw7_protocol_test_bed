### ID: REQ-DW8-072

- **Title:** Simplify and Refine AI Context Refresh Protocol
- **Status:** `Pending`
- **Priority:** `Critical`
- **Details:** The context provided to the AI at each cycle is too verbose and includes raw, misleading bug logs. This protocol needs to be updated to provide a concise, high-level summary to prevent context decay and improve focus.
- **SMRs:**
  - [ ] **SMR-DW8-072.1:** Modify the context generation script to summarize previous achievements instead of listing all changes.
  - [ ] **SMR-DW8-072.2:** Modify the context generation script to summarize the next steps clearly.
  - [ ] **SMR-DW8-072.3:** Remove raw exception tracebacks from the mandatory context refresh.
  - [ ] **SMR-DW8-072.4:** Ensure the AI Protocol Tutorial remains a core part of the context.