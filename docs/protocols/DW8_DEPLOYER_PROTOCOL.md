# DW8 Protocol: The Deployer Stage

This document formalizes the complete vision for the `Deployer` stage, transforming it from a placeholder into a robust, automated deployment and versioning engine. It addresses two critical scenarios: standard project deployment and protocol evolution deployment.

## 1. Core Principle

The `Deployer` stage is the final step in every development cycle. Its primary responsibility is to ensure that all work is durably stored, versioned, and, where applicable, officially released. It must handle both the project's own codebase and the evolution of the DW protocol itself, using the `github-mcp-server` to avoid manual authentication and automate all Git operations.

## 2. Scenario A: Standard Project Deployment

This is the default behavior for any project that is **not** updating the DW protocol itself.

1. **End-of-Cycle Push:** At the conclusion of every development cycle (i.e., when a requirement is moved to `Deployed`), the `Deployer` will automatically commit and push all changes in the project directory to its designated Git repository.
2. **Repository Creation:** If the target repository does not exist, the `Deployer` will use the `github-mcp-server` to create it automatically.
3. **Versioning:** Each end-of-cycle push will be versioned using a Git tag (e.g., `v1.1`, `v1.2`, etc.) to create a clear history of completed requirements.
4. **Final Documentation:** Upon completion of the *entire project* (all requirements are `Deployed`), the `Deployer` will generate a comprehensive `README.md`. This file will include an overview of the project, installation instructions, usage guides, and API/function documentation. This `README.md` will be included in the final push.

## 3. Scenario B: Protocol Evolution Deployment

This scenario is triggered when the `is_protocol_update` flag is `true`.

1. **Dual-Push Mandate:** The `Deployer` must perform **two** distinct push operations at the end of every cycle:
    - **Push 1 (Test Bed):** Commit and push the changes from the current project directory (e.g., `dw7_protocol_test_bed`) to its own repository, following the standard versioning procedure.
    - **Push 2 (Official Protocol):** Commit and push the updated workflow logic to the official `windsurf-development-workflow` repository. This ensures that valuable improvements to the protocol are never lost and are versioned centrally.
2. **Protocol Synchronization:** Before pushing to the official repository, the `Deployer` must first copy the finalized source code (e.g., from `src/dw6`) to the official versioned protocol directory (e.g., `/home/ubuntu/devs/dw/dw8`).

## 4. Configuration and Credential Management

To power this automation, the `Deployer` will rely on a new configuration system:

1. **Credential Setup:** On first use with a new user/project, the workflow will prompt for Git credentials. These credentials will be stored securely in a local `.env` file.
2. **MCP Integration:** The user will be asked for permission to configure the `github-mcp-server` with these credentials, enabling seamless, non-interactive Git operations in the future.
3. **Configuration File:** A new file, `docs/DEPLOYER_CONFIGURATION.md`, will be created to store all necessary paths and URLs, such as the official protocol directory, the official repository URL, and the project-specific repository URL. The `DeployerStage` will read this file to get its operational parameters.
