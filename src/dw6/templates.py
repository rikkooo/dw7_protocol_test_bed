# src/dw6/templates.py

TECHNICAL_SPECIFICATION_TEMPLATE = """
# Technical Specification: {title}

**Requirement ID:** {req_id}
**Date:** {date}

## 1. Overview

*A brief, one-paragraph summary of the feature or bug to be addressed.*

## 2. Rationale

*Why is this change necessary? What is the business or technical driver?*

## 3. Proposed Solution

*A detailed description of the proposed implementation. This should cover:
- Which files/modules will be created or modified.
- Key classes, functions, or data structures to be added.
- Any changes to the UI, API, or data models.*

## 4. Task Breakdown

*A checklist of the individual engineering tasks required to complete the work.*

- [ ] Task 1: ...
- [ ] Task 2: ...
- [ ] Task 3: ...

## 5. Testing Plan

*How will this feature be tested? This should include:
- Unit tests for new functions/classes.
- Integration tests for how the new code interacts with existing code.
- Manual testing steps, if applicable.*

## 6. Risks and Mitigations

*What are the potential risks (e.g., performance impact, breaking changes), and how will they be mitigated?*

"""
