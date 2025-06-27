# DW8 Protocol: Robust Command Output Handling

## 1. Principle

To ensure the AI agent can make accurate, evidence-based decisions, all critical shell commands must be executed in a way that guarantees the capture of their complete, untruncated output. This protocol formalizes the procedure for achieving this, preventing the misdiagnosis of failures due to incomplete information.

## 2. The Trigger

This protocol must be used whenever the outcome of a shell command is critical for a validation step or a key decision. This includes, but is not limited to:

- Running test suites (e.g., `pytest`).
- Complex build or compilation scripts.
- Any command whose output needs to be parsed or checked for specific results.

## 3. The Procedure

The agent will execute the following three-step process:

1. **Execute and Redirect:** The command will be executed using the `run_command` tool. The command string must include redirection of both `stdout` and `stderr` to a temporary log file. For example: `my_critical_command > command_output.log 2>&1`.
2. **Read Full Output:** Immediately after the command completes, the agent will use the `mcp3_read_file` tool to read the entire contents of the temporary log file. This provides a complete and untruncated record of the command's execution.
3. **Analyze and Clean Up:** The agent will analyze the captured output to determine the outcome. After the analysis is complete, the agent should delete the temporary log file to maintain a clean working directory.
