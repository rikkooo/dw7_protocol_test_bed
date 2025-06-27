# Deployer Stage Configuration

This file contains the configuration parameters for the DW8 Deployer stage. The workflow reads this file to manage automated Git operations and protocol evolution.

## 1. Project Repository

- **PROJECT_REPO_URL:** `https://github.com/your-username/your-project-repository.git`

## 2. Protocol Evolution Settings

These settings are only used when `is_protocol_update` is `true`.

- **OFFICIAL_PROTOCOL_DIR:** `/home/ubuntu/devs/dw/dw8`
- **OFFICIAL_PROTOCOL_REPO_URL:** `https://github.com/windsurf-ai/windsurf-development-workflow.git`
