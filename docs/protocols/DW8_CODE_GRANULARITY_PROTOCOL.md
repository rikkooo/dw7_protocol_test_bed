# DW8 Protocol: Code Granularity

## 1. Principle

To improve the reliability of AI-driven code modifications, large source code files will be refactored into a more granular "interface/implementation" structure. This ensures that the AI agent's context is always focused and accurate when performing file edits, minimizing errors caused by context drift.

## 2. The Trigger

This refactoring protocol should be applied to any source code file that exceeds **150 lines** of code.

## 3. The Refactoring Procedure

When a file is refactored, the following steps must be taken:

1. **Create Implementation Directory:** A new directory is created alongside the original file. The directory name is a concise, deterministic abbreviation of the original filename (e.g., `deployer.py` -> `dp/`).
2. **Extract Methods:** Each function or class method from the original file is moved into its own separate Python file inside the new implementation directory. The filename is an abbreviation of the function name (e.g., `_execute_protocol_evolution` -> `exec_proto_evo.py`).
3. **Create Interface File:** The original file becomes the "interface." Its contents are replaced with logic that dynamically imports all the functions/methods from the implementation directory and attaches them to the appropriate class or module scope.

## 4. Naming Convention

- **Directories:** A 2-3 letter abbreviation of the source file. E.g., `deployer.py` -> `dp/`.
- **Files:** A snake_case abbreviation of the function name. E.g., `_check_if_project_is_complete` -> `chk_proj_cpl.py`.
