# [P] [M] REQ-DW8-014: Implement Code Granularity Protocol to Improve Edit Reliability

## 1. Requirement

To mitigate frequent `edit_file` failures caused by context drift and large file sizes, implement a "Code Granularity Protocol" that refactors large source code files into a more manageable, "header/implementation" structure.

## 2. Rationale

The AI agent frequently fails to apply edits to large files because the `oldText` parameter does not perfectly match the file's current content. This is due to the inherent limitations of the context window and the difficulty of recalling exact text from large files. This leads to wasted resources, repeated attempts, and project delays. By breaking down large files into smaller, function-level files, we can ensure the AI's context is always fresh and accurate before an edit, drastically improving the success rate of write operations.

## 3. Sub-Meta-Requirements (SMRs)

- **SMR-DW8-014.1:** **Define Refactoring Trigger:** Establish a clear trigger for refactoring, such as a maximum line count (e.g., 200 lines) or file size threshold.
- **SMR-DW8-014.2:** **Develop Refactoring Logic:** Implement a workflow or tool that can automatically split a large class/module file into an "interface" file and a directory of smaller "implementation" files (one per function/method).
- **SMR-DW8-014.3:** **Define Naming Convention:** Create a deterministic and concise naming convention for the new implementation directories and files (e.g., `deployer.py` -> `dp/`, `_load_config` -> `ld_cfg.py`).
- **SMR-DW8-014.4:** **Update Code Interpreter:** Modify the AI's core logic to recognize and work with this new file structure. When tasked with editing a function, it must first locate and read the small implementation file, not the large interface file.
- **SMR-DW8-014.5:** **Update Importer Logic:** The "interface" file should dynamically import the functions from their implementation files to ensure the public-facing API remains unchanged and the code remains executable.
- **SMR-DW8-014.6:** **Create a "Refactoring Stage":** Introduce a new, optional stage in the workflow that can be triggered manually or automatically to perform this refactoring on specified files.

## 4. Acceptance Criteria

- The system can identify files that exceed the defined complexity threshold.
- The system can refactor a large Python file into the new interface/implementation structure.
- The AI agent can successfully locate, read, and edit a function within the new granular structure with a significantly higher success rate than before.
- The refactored code remains fully functional and passes all existing tests.
