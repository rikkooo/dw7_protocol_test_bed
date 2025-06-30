# Design Document: Composable Manual Build System

## 1. Objective

To create a simple, robust build script that assembles the distributed manual chapters into a single, concatenated Markdown file. This provides the AI with a single source of truth for 'total recall' while allowing developers to maintain small, focused chapter files.

## 2. System Components

1.  **Master Index File (`docs/AI_OPERATIONS_MANUAL.md`):** A Markdown file that acts as an ordered list of paths to the individual chapter files.
2.  **Chapter Files (`docs/manual_chapters/*.md`):** The individual, granular content files.
3.  **Build Script (`scripts/build_manual.py`):** A Python script that orchestrates the assembly.
4.  **Compiled Output (`docs/AI_OPERATIONS_MANUAL.compiled.md`):** The temporary, single-file output of the build process. This file should be added to `.gitignore`.

## 3. Logic and Flow

### 3.1. Master Index Format

The `docs/AI_OPERATIONS_MANUAL.md` will be a simple list of relative paths:

```markdown
# AI Operations Manual - Master Index

This file lists the chapters of the manual in their canonical order.

- manual_chapters/01_vision_and_mission.md
- manual_chapters/02_system_architecture.md
- manual_chapters/03_state_machine.md
- manual_chapters/04_key_protocols.md
- manual_chapters/05_kernel_api.md
- manual_chapters/06_state_manager_api.md
- manual_chapters/07_operational_commands.md
```

### 3.2. Build Script (`scripts/build_manual.py`)

The script will perform the following actions:

1.  **Argument Parsing:** It will accept no arguments and will have hardcoded paths for the index and output files, relative to the project root.
2.  **Read Master Index:** It will open `docs/AI_OPERATIONS_MANUAL.md` and parse it to extract the list of chapter file paths.
3.  **Initialize Output:** It will open `docs/AI_OPERATIONS_MANUAL.compiled.md` in write mode, clearing any previous content.
4.  **Concatenate Chapters:** It will iterate through the list of chapter paths in order. For each path:
    a. It will open and read the entire content of the chapter file.
    b. It will write the content to the output file.
    c. It will write a separator (e.g., `\n\n---\n\n`) between chapters to ensure clear visual separation in the final compiled file.
5.  **Completion Message:** Upon success, it will print a confirmation message to the console, e.g., `"Successfully compiled 7 chapters into AI_OPERATIONS_MANUAL.compiled.md"`.

### 3.3. Trigger Command

The Governor will trigger this script using a standard command:

`uv run python scripts/build_manual.py`

This command will be executed as the first step of the 'Total Recall' protocol.

## 4. Implementation Sketch

```python
# scripts/build_manual.py

import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
INDEX_PATH = os.path.join(PROJECT_ROOT, 'docs', 'AI_OPERATIONS_MANUAL.md')
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'docs', 'AI_OPERATIONS_MANUAL.compiled.md')
CHAPTERS_DIR = os.path.join(PROJECT_ROOT, 'docs') # Chapters are relative to docs dir

def main():
    print("Starting manual compilation...")
    
    try:
        with open(INDEX_PATH, 'r') as f:
            index_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Master index file not found at {INDEX_PATH}")
        return

    # Find all markdown links which are our chapters
    chapter_paths = re.findall(r'\((manual_chapters/.*?\.md)\)', index_content)

    if not chapter_paths:
        print("ERROR: No chapter files found in the master index.")
        return

    with open(OUTPUT_PATH, 'w') as outfile:
        for i, rel_path in enumerate(chapter_paths):
            chapter_full_path = os.path.join(CHAPTERS_DIR, rel_path)
            try:
                with open(chapter_full_path, 'r') as infile:
                    outfile.write(infile.read())
                    # Add a separator, but not after the last file
                    if i < len(chapter_paths) - 1:
                        outfile.write('\n\n---\n\n')
            except FileNotFoundError:
                print(f"WARNING: Chapter file not found, skipping: {chapter_full_path}")

    print(f"Successfully compiled {len(chapter_paths)} chapters into {os.path.basename(OUTPUT_PATH)}")

if __name__ == "__main__":
    main()

```
