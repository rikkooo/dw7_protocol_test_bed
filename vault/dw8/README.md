# DW8 Protocol

## Overview
The DW8 protocol represents an evolution in the development workflow, focusing on robustness, self-reflection, and automated release management.

## Workflow Diagram
`Engineer` -> `Coder` -> `Validator` -> `Deployer`
   ^            |
   |         (failure)
   +------- `Rehearsal`

## Version Changelog (vs DW7)
- **Implemented `Rehearsal` State:** A mandatory 'time-out' state triggered by consecutive failures.
- **Formalized Protocol Evolution:** The `Deployer` stage now includes a sub-workflow to automatically version, document, and release new protocol updates.