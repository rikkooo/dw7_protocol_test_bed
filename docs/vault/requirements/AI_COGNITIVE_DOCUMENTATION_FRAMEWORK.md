# The AI-Cognitive Documentation Framework (AI-CDF)

## 1. Principle

The AI-Cognitive Documentation Framework (AI-CDF) is a system for creating and maintaining project documentation that is specifically optimized for consumption by AI agents. It addresses the common failure modes of AI, such as context decay, 'laziness' in following linked resources, and the need for both rapid, task-specific context and deep, system-wide context.

The framework is built on three core pillars designed to ensure the AI agent always has the right level of information at the right time.

---

## Pillar 1: The Dynamic Mission Brief (For Fast Recall)

**Objective:** To provide minimal, relevant, and just-in-time context for the AI's current task, preventing cognitive overload while ensuring accuracy.

**Implementation:**

1. **`PROJECT_SUMMARY.md`**: A single, high-level file containing the project's core mission, vision, and purpose. This serves as the AI's 'North Star' and is provided during initial context loading.

2. **`_CONTEXT.md` Files**: Small, focused Markdown files placed within key functional directories (e.g., `src/dw6/workflow/kr/`, `src/dw6/st/`).

3. **Dynamic Loading**: Before the AI begins work on any file within a directory containing a `_CONTEXT.md` file, the system will automatically prepend the contents of that file to the AI's instructions. This file will contain:
    * The specific purpose of the module.
    * An overview of key classes, methods, and their interactions.
    * Critical 'gotchas', design patterns, or warnings.

4. **Explicit Warnings**: The context will include a direct, attention-grabbing warning, such as: `*** GEM, READ THIS! *** If you are stuck, you MUST consult the full Operations Manual before trying again.`

---

## Pillar 2: The Composable Manual (For Total Recall)

**Objective:** To provide a single, comprehensive source of truth for full context recovery, while maintaining low-cost, granular updates.

**Implementation:**

1. **Distributed Chapters**: The manual's content is stored in small, focused chapter files within a `docs/manual_chapters/` directory (e.g., `01_vision.md`, `02_architecture.md`). This makes updates cheap and targeted.

2. **Master Index (`AI_OPERATIONS_MANUAL.md`)**: This file does not contain content itself, but acts as an ordered 'playlist' or index, listing the paths to the chapter files in the correct sequence.

3. **'Total Recall' Build Script**: A script (`scripts/build_manual.py`) is responsible for assembling the complete manual on demand. When a total recall is needed, the Governor runs this script to concatenate all chapters into a single, temporary `AI_OPERATIONS_MANUAL.compiled.md` file.

4. **Recovery Protocol**: The AI's instruction for a total recall is to read the single, compiled `.md` file. This provides the ease of a monolithic document for the AI, with the maintainability of distributed files for the developers.

---

## Pillar 3: The 'Smart' Living Documentation Protocol (For 'Model Homework')

**Objective:** To ensure documentation is treated as a core deliverable by intelligently linking code context to specific manual chapters.

**Implementation:**

1. **Context-to-Chapter Linking**: Each `_CONTEXT.md` file will contain a metadata header linking it to its corresponding manual chapter (e.g., `Manual-Chapter: 05_kernel_api.md`).

2. **Mandatory Deployer Check**: A new validation step will be added to the `Deployer` stage.

3. **The Governor's 'Smart' Query**: The Governor will parse the `_CONTEXT.md` file for the current task, find the linked chapter, and ask a highly specific question: `"The _CONTEXT.md for this module has been updated. Have you also updated its linked chapter, 'docs/manual_chapters/05_kernel_api.md'?"`

4. **Targeted Validation**: This makes the validation process extremely efficient and low-cost, focusing the AI's attention on the single chapter that needs updating, rather than the entire manual.
