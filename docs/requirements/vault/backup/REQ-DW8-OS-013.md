# REQ-DW8-OS-013: [Execution] Enhance `WorkflowState` with Event Queue Management

- **Priority:** [C]
- **Status:** [P]
- **Type:** Execution

## 1. Description

To resolve the "dual source of truth" problem identified in `REQ-DW8-OS-002`, the `WorkflowState` class must be enhanced to become the sole manager of the event queues. It will no longer be just a simple key-value store but a comprehensive state and queue management object.

## 2. Acceptance Criteria

- A new method `add_pending_event(self, event, priority)` is added to `WorkflowState`. This method will encapsulate the logic for adding a new event to the `PendingEvents` list according to its priority.
- A new method `archive_completed_event(self)` is added to `WorkflowState`. This method will move the currently active event from the `PendingEvents` list to a new `ProcessedEvents` list within the state data.
- The `WorkflowState` class will now manage both `PendingEvents` and `ProcessedEvents` lists within its internal `self.data` dictionary.