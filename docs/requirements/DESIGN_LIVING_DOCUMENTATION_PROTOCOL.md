# Design Document: Living Documentation Protocol

## 1. Objective

To implement a protocol that ensures project documentation is treated as a first-class deliverable and is kept synchronized with the source code. This system, a core component of the AI-CDF's 'Pillar 3', makes documentation updates a mandatory, non-negotiable part of the development workflow.

## 2. System Components

1.  **The Governor**: The master controller will be responsible for enforcing the documentation check.
2.  **The Deployer Stage**: The final stage of the workflow will be modified to include this new validation step.

## 3. Logic and Flow

The protocol will be implemented as a new validation gate within the `Deployer` stage.

### 3.1. Trigger

The documentation check will be triggered when the `approve` command is issued while the workflow is in the `Deployer` stage, just before the final deployment actions are executed.

### 3.2. The Validation Gate: `_validate_documentation_update`

1.  A new private method, `_validate_documentation_update`, will be added to the `Governor`.
2.  The `DeployerStage.approve` method will be modified to call this `Governor` method before proceeding with its core logic.
3.  This method will pose a direct, non-skippable question to the AI agent.

#### 3.3. Context-to-Chapter Linking

A new private method in the Governor, `_get_linked_manual_chapter`, will be responsible for parsing the `_CONTEXT.md` file associated with the current task. It will use a simple regex or string search to find the `Manual-Chapter:` metadata header and return the linked chapter's filename.

### 3.4. The Governor's 'Smart' Query

If a linked chapter is found, the Governor will formulate a highly specific query:

```
*** LIVING DOCUMENTATION PROTOCOL CHECK ***

The _CONTEXT.md for this module has been updated. Have you also updated its linked chapter, 'docs/manual_chapters/[linked_chapter_filename.md]'?

Please respond with 'Yes' or 'No'. If 'Yes', provide a brief, one-sentence summary of the documentation changes made.
```

If no link is found, a general query will be used as a fallback.

### 3.4. Success and Failure Criteria

The Governor will parse the AI's response to determine if the gate passes.

*   **Success Condition:**
    *   The AI's response starts with `"Yes"` (case-insensitive).
    *   The AI provides a plausible, non-empty summary following the confirmation.
    *   If successful, the `_validate_documentation_update` method returns `True`, and the `Deployer` stage proceeds.

*   **Failure Condition:**
    *   The AI's response starts with `"No"`.
    *   The AI's response is evasive, irrelevant, or does not follow the required format.
    *   If failed, the method returns `False`. The `Deployer` stage is blocked, and the Governor issues the following message to the user/AI: `"LIVING DOCUMENTATION PROTOCOL FAILED: Documentation update not confirmed. Please update the relevant documentation before re-attempting deployment approval."`

## 4. Implementation Sketch

```python
# In governor.py

class Governor:
    # ... existing methods ...

    def _get_linked_manual_chapter(self, context_content):
        import re
        match = re.search(r"^Manual-Chapter:\s*(.*\.md)", context_content, re.MULTILINE)
        return match.group(1) if match else None

    def _validate_documentation_update(self, ai_response, context_content):
        linked_chapter = self._get_linked_manual_chapter(context_content)
        # The Governor would use this linked_chapter to formulate the specific prompt

        response_lower = ai_response.lower().strip()
        if response_lower.startswith('yes'):
            if len(response_lower) > 10:
                print(f"--- Governor: Documentation update for {linked_chapter or 'docs'} confirmed. ---")
                return True
        
        print("--- Governor: LIVING DOCUMENTATION PROTOCOL FAILED: Documentation update not confirmed. ---")
        return False

# In deployer_stage.py (conceptual)

class DeployerStage:
    def __init__(self, governor):
        self.governor = governor

    def approve(self, ai_confirmation_response):
        if not self.governor._validate_documentation_update(ai_confirmation_response):
            print("Please update the relevant documentation before re-attempting deployment approval.")
            return
        
        # ... proceed with deployment logic ...
        print("Deployment proceeding...")
```
