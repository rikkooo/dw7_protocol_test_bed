# Design Document: Dynamic Mission Brief System

## 1. Objective

To implement a system that automatically provides the AI agent with focused, relevant context based on the file(s) it is currently working on. This system, a core component of the AI-CDF's 'Pillar 1', aims to improve the AI's accuracy and reduce context-related errors by delivering just-in-time 'mission briefings'.

## 2. System Components

1.  **The Governor**: The central controller of the workflow will be responsible for orchestrating the context-loading process.
2.  **`_CONTEXT.md` files**: Small, Markdown-based files placed strategically within the project's directory structure.

## 3. Logic and Flow

The system will operate based on a simple, robust directory traversal algorithm.

### 3.1. Trigger

The context-loading process will be triggered whenever the AI's task is associated with a specific file path. This includes, but is not limited to:
-   When the user's prompt explicitly references a file.
-   When the AI proposes a file-based tool call (e.g., `edit_file`, `view_line_range`).

### 3.2. Context Discovery Algorithm

1.  The Governor receives the target file path (e.g., `/home/ubuntu/devs/dw7_protocol_test_bed/src/dw6/workflow/kr/advance_stage.py`).
2.  It extracts the directory of the target file (e.g., `.../kr/`).
3.  The Governor begins to traverse **up** the directory tree from the current directory.
4.  In each directory it visits, it checks for the existence of a file named `_CONTEXT.md`.
5.  The search stops as soon as the **first** `_CONTEXT.md` file is found. This ensures that the most specific, closest context is always prioritized.
    *   *Example*: If both `.../kr/_CONTEXT.md` and `.../workflow/_CONTEXT.md` exist, the system will load `.../kr/_CONTEXT.md` and ignore the other.
6.  If the traversal reaches the project root without finding a `_CONTEXT.md` file, no dynamic context is loaded for that turn.

### 3.3. Context Injection

1.  Once a `_CONTEXT.md` file is found, its entire content is read by the Governor.
2.  The content is then prepended to the instructions or prompt being sent to the AI for the current turn.
3.  The injected context will be clearly demarcated to be easily identifiable by the AI:

    ```
    *** DYNAMIC MISSION BRIEF LOADED ***
    Source: [Full path to the loaded _CONTEXT.md file]

    [... content of _CONTEXT.md ...]

    *** END OF BRIEF ***
    ```

## 4. Implementation Sketch

The logic will be encapsulated within a new method in the `Governor` class.

```python
# In governor.py

class Governor:
    # ... existing methods ...

    def _get_dynamic_context(self, target_file_path):
        import os
        current_dir = os.path.dirname(target_file_path)
        project_root = '/home/ubuntu/devs/dw7_protocol_test_bed' # This should be configurable

        while project_root in current_dir:
            context_file = os.path.join(current_dir, '_CONTEXT.md')
            if os.path.exists(context_file):
                with open(context_file, 'r') as f:
                    content = f.read()
                return f'*** DYNAMIC MISSION BRIEF LOADED ***\nSource: {context_file}\n\n{content}\n*** END OF BRIEF ***\n'
            
            # Move up one directory
            if current_dir == project_root:
                break
            current_dir = os.path.dirname(current_dir)
            
        return '' # No context found

    def process_request(self, user_request, target_file=None):
        dynamic_context = ''
        if target_file:
            dynamic_context = self._get_dynamic_context(target_file)
        
        full_prompt = dynamic_context + user_request
        # ... send full_prompt to AI ...
```
