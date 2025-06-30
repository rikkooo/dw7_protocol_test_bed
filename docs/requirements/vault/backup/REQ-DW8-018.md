# REQ-DW8-018 - Implement Project Statistics Tracking

**Type:** Standard
**Status:** Pending

## Description

The workflow should track and report on various project statistics, including time tracking, token consumption, requirement counts, and failure rates.

## Acceptance Criteria

- [ ] The `WorkflowState` class is extended to include a `statistics` dictionary.
- [ ] The `statistics` object tracks `total_requirements_completed`, `total_requirements_pending`, and `failure_rates_by_stage`.
- [ ] The kernel logs the start and end time for each stage transition for a given requirement.
- [ ] The kernel calculates and stores the duration spent in each stage for each requirement.
- [ ] The kernel increments the `total_requirements_completed` and decrements `total_requirements_pending` when a requirement is moved to the processed queue.
- [ ] The `increment_failure_counter` method in `WorkflowState` is updated to log the stage and timestamp of each failure.
- [ ] A new CLI command, `stats`, is created to display the collected project statistics in a clear, formatted report.