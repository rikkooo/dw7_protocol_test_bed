# System Identity & Recovery Briefing

**TO:** Cascade AI Agent
**FROM:** DW8 Governor
**SUBJECT:** Mission Context & Recovery Protocol

This briefing is your single source of truth for re-establishing your operational parameters.

## 1. Mission Recall: Your Core Objective

- **Project Name:** `dw7_protocol_test_bed`
- **Primary Mission:** You are the lead agent upgrading our autonomous development framework from version DW7 to DW8. You are building **the factory that builds applications.**
- **Human Partner:** Your operator is Riko.

## 2. The Golden Rule: Engage the Workflow

You **must** operate inside the established workflow. Do not attempt to "fix" the system.

## 3. The 3-Step Recovery Procedure

This is the **only** approved method for re-engaging the workflow.

### Step 1: Identify Active Requirement

```bash
cat data/workflow_state.json
```

### Step 2: Load Workflow Context

```bash
uv run dw6 status
```

### Step 3: Understand Your Specific Task

```bash
cat events/<Active_Requirement_ID>.json

---

### How to Create a New Requirement

To create a new requirement in the DW8 protocol, use the `dw6 new` command. This command formalizes a new task and injects it into the workflow's event queue.

**Command Structure:**

```bash
uv run dw6 new <REQUIREMENT_ID> -t "<TITLE>" -d "<DESCRIPTION>" -a "<CRITERION_1>" "<CRITERION_2>" ... --priority <PRIORITY>
```

**Parameters:**

*   **`<REQUIREMENT_ID>`** (Required): A unique identifier for the requirement (e.g., `REQ-DW8-FEATURE-001`).
*   **`-t` or `--title`** (Required): A short, descriptive title for the requirement, enclosed in quotes.
*   **`-d` or `--description`** (Required): A detailed description of the task, enclosed in quotes.
*   **`-a` or `--acceptance-criteria`** (Required): A list of one or more specific, testable criteria that must be met for the requirement to be considered complete. Each criterion should be enclosed in its own set of quotes.
*   **`--priority`** (Optional): Sets the priority of the requirement. Can be `High`, `Medium`, or `Low`. Defaults to `Low`.

**Example:**

```bash
uv run dw6 new REQ-DW8-API-005 -t "Implement user authentication endpoint" -d "Create a new POST endpoint at /api/login that accepts a username and password." -a "Endpoint returns a JWT token on success." "Endpoint returns a 401 error on failure." --priority High
```

**Output:**

Upon successful execution, this command automatically creates a new JSON file in the `events/` directory. The file will be named according to the requirement ID provided.

For the example above, the created file would be: `events/REQ-DW8-API-005.json`.

This file contains all the details of the requirement and is now part of the formal workflow queue.
