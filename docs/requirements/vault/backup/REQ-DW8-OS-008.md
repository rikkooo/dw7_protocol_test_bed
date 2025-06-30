# REQ-DW8-OS-008: [Execution] Implement Decoupled Deployer Logic

- **Priority:** [M]
- **Status:** [P]
- **Type:** Execution

## 1. Description

To increase workflow efficiency, this requirement decouples the `Deployer` stage from the standard event cycle. Most events will no longer require a deployment step. Deployment will become a special, dedicated event type that can be scheduled independently, making normal cycles faster and more lightweight.

## 2. Acceptance Criteria

- The Kernel's `advance_stage` logic is modified to end a standard cycle after the `Validator` stage.
- A new event type, `DeploymentEvent`, is created.
- When the Kernel processes a `DeploymentEvent`, it invokes the `Deployer` stage.
