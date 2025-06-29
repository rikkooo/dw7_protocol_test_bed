# Chapter 3: Key Protocols

## 3.1. The State Machine Protocol

The entire workflow is governed by a strict, explicit state machine. The system can only be in one of the following states at any given time:

- **IDLE:** The system is waiting for a command.
- **ENGINEER:** The AI is in a planning and design phase. Code modification is forbidden.
- **CODER:** The AI is in the implementation phase. Code modification is permitted.
- **VALIDATOR:** The AI is in a testing and validation phase.
- **DEPLOYER:** The AI is preparing the code for release and performing final checks.

The Governor is responsible for all state transitions. Transitions are only allowed in a predefined sequence (e.g., Coder -> Validator -> Deployer). Any attempt to perform an action not allowed in the current state will be rejected.

## 3.2. The AI-Cognitive Documentation Framework (AI-CDF)

This is the master protocol for managing the AI's long-term memory and context. It is composed of three pillars:

1.  **Dynamic Mission Briefs (`_CONTEXT.md`):** Provide immediate, just-in-time context for specific tasks.
2.  **The Composable Operations Manual:** Provides a mechanism for total project recall through a buildable, comprehensive manual.
3.  **The 'Smart' Living Documentation Protocol:** Enforces that documentation is updated as a mandatory part of the development lifecycle.

## 3.3. The 'Smart' Living Documentation Protocol

This protocol ensures that the Operations Manual never becomes stale. It is a hard gate in the `Deployer` stage.

- **Mechanism:** Before a deployment can be approved, the Governor checks if a `_CONTEXT.md` file was modified. If so, it finds the linked master chapter via metadata (`Manual-Chapter: ...`) and asks the AI to confirm that the corresponding chapter has also been updated.
- **Purpose:** This creates a direct, low-cost, and enforceable link between code changes and documentation updates, ensuring the long-term health of the project's knowledge base.
