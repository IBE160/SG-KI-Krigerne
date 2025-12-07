# Story 2.1: Implement Natural Language Query Input

**Epic:** [2 - Core Question Answering](docs/epics.md)
Status: review
**Points:** (TBD - estimate during sprint planning)
**Author:** BIP

## User Story

As a **User**,
I want **to ask questions about course information in natural language**,
So that **I can find information without needing to know specific commands or keywords**.

## Acceptance Criteria

*(Source: [docs/epics.md#Story 2.1](docs/epics.md))*

1.  **Given** the user has entered a question (e.g., "what is the exam format for TDT4140?"),
2.  **When** they send the message,
3.  **Then** the system backend receives the raw text of the question.
4.  **And** the backend identifies the user's core intent (e.g., `get_exam_format`) and the key entity (e.g., `course_code: TDT4140`).

## Tasks / Subtasks

- [x] **Task 1: Design and Implement FastAPI Endpoint for Natural Language Query (AC: 1, 2, 3)**
    - [x] Subtask 1.1: Create a new file `backend/src/api/chat.py` to house the chat endpoint.
    - [x] Subtask 1.2: Define a `POST /chat` endpoint in `backend/src/api/chat.py` that accepts a JSON payload with a `query` string (e.g., `{"query": "what is the exam format for TDT4140?"}`).
    - [x] Subtask 1.3: Integrate the new `chat` router into `backend/main.py`.
    - [x] Subtask 1.4: Implement a basic placeholder response for the endpoint (e.g., echoing the received query) to verify connectivity.
- [x] **Task 2: Implement Intent and Entity Extraction Logic (AC: 4)**
    - [x] Subtask 2.1: Create a new file `backend/src/rag/query_parser.py` for query parsing logic.
    - [x] Subtask 2.2: Implement a function in `query_parser.py` that takes a natural language `query` string as input.
    - [x] Subtask 2.3: Use simple keyword matching or regex to identify core intent (e.g., `get_exam_format`, `get_learning_outcomes`, `get_mandatory_assignments`) and extract relevant entities (e.g., `course_code: TDT4140`).
    - [x] Subtask 2.4: Define a clear output structure for the parsed intent and entities (e.g., a Pydantic model).
    - [x] Subtask 2.5: Integrate the `query_parser.py` into the `POST /chat` endpoint to process the incoming query.
- [x] **Task 3: Write Backend Tests (Pytest)**
    - [x] Subtask 3.1: Create a test file `backend/tests/test_chat_api.py`.
    - [x] Subtask 3.2: Write a test for the `POST /chat` endpoint to ensure it receives a query and returns a placeholder response. (AC: 1, 2, 3)
    - [x] Subtask 3.3: Create a test file `backend/tests/test_query_parser.py`.
    - [x] Subtask 3.4: Write unit tests for `query_parser.py` to verify correct intent and entity extraction for various natural language queries. (AC: 4)
        - Test case: "what is the exam format for TDT4140?" -> intent: `get_exam_format`, entity: `course_code: TDT4140`
        - Test case: "learning outcomes for MAT100" -> intent: `get_learning_outcomes`, entity: `course_code: MAT100`
        - Test case: "mandatory assignments for LOG200" -> intent: `get_mandatory_assignments`, entity: `course_code: LOG200`

## Dev Notes

### Requirements and Constraints Summary
- **Functional Requirements Covered:** FR1.
- This story is the entry point for the RAG pipeline.
- The initial implementation for intent and entity extraction can use simple keyword matching or regex.
- Backend API pattern will be REST, expecting a JSON payload with the query.

### Learnings from Previous Story
**From Story 1.4: Implement Real-Time Message Handling in the UI (Status: done)**

The previous story established the frontend UI components and structure for message handling. The `ChatWindow.tsx` component is the client-side integration point for this story's backend endpoint.

**CRITICAL: Unresolved Review Items from Story 1.3**
The following action items from the review of Story 1.3 are still pending and must be considered in future UI-related stories, as they impact the overall quality and accessibility of the chat interface:
- [ ] [Medium] Implement robust automated tests for desktop responsiveness
- [ ] [Medium] Implement robust automated tests for mobile responsiveness
- [ ] [Medium] Implement robust automated tests for keyboard navigation accessibility
- [ ] [Medium] Implement robust automated tests for color contrast accessibility
- [ ] [Medium] Implement robust automated tests for `aria-labels` accessibility

### Project Structure Notes
- All backend implementation will be within the `backend/` directory, following Python `snake_case` for variables/functions and `PascalCase` for classes.
- New files will be created in `backend/src/api/chat.py`, `backend/src/rag/query_parser.py`, `backend/tests/test_chat_api.py`, and `backend/tests/test_query_parser.py`.

### References
- [Source: docs/epics.md#Story 2.1: Implement Natural Language Query Input (MVP)]
- [Source: docs/architecture.md#Backend-API-Pattern]
- [Source: docs/architecture.md#AI-Application]
- [Source: docs/architecture.md#Project-Structure]
- [Source: docs/sprint-artifacts/1-4-implement-real-time-message-handling-in-the-ui.md#Senior-Developer-Review-(AI)]

## Dev Agent Record

### Context Reference
- `docs/sprint-artifacts/2-1-implement-natural-language-query-input.context.xml`

### Agent Model Used
{{agent_model_name_version}}

### Debug Log References
- [[debug-log-2025-12-03-1.txt]]

### Completion Notes List
- Implemented the `/chat` endpoint in FastAPI.
- Created a query parser to extract intent and entities from natural language queries.
- Added unit tests for the new endpoint and the query parser.
- Resolved dependency issues related to Pydantic and Python 3.13 by installing Rust and upgrading dependencies.

### File List
- `backend/src/api/chat.py`
- `backend/src/rag/query_parser.py`
- `backend/tests/test_chat_api.py`
- `backend/tests/test_query_parser.py`
- `backend/main.py` (modified)
- `backend/requirements.txt` (modified)


## Change Log
- **Date:** December 3, 2025
- **Description:** Initial draft of Story 2.1 created from `epics.md`, `prd.md`, `architecture.md`, and `ux-design-specification.md`. Lessons learned from Story 1.4 incorporated.
- **Date:** December 3, 2025
- **Description:** Implemented the `/chat` endpoint, query parser, and tests. Marked story as 'review'.

## Senior Developer Review (AI)

**Reviewer:** BIP
**Date:** 2025-12-03
**Outcome:** Approve

**Summary:** The story successfully implements the FastAPI endpoint for natural language query input, including intent and entity extraction using basic keyword matching and regex, as specified for the MVP. All acceptance criteria are met, and all tasks are verified complete. The implementation includes appropriate unit and integration tests. A minor Pydantic deprecation warning was noted in an existing test file (`test_knowledge_base_manager.py`), but this is outside the scope of this story's changes.

### Key Findings (by severity):
*   **LOW:** Existing `backend/tests/test_knowledge_base_manager.py` uses `dummy_course.dict()` which triggers a `PydanticDeprecatedSince20` warning. This should be updated to `model_dump()` for Pydantic v2 compatibility in a separate cleanup task. (file: `backend/tests/test_knowledge_base_manager.py`)

### Acceptance Criteria Coverage:
| AC# | Description                                                               | Status      | Evidence                                                              |
| :-- | :------------------------------------------------------------------------ | :---------- | :-------------------------------------------------------------------- |
| 1   | Given the user has entered a question                                     | IMPLEMENTED | `backend/src/api/chat.py:10`, `backend/tests/test_chat_api.py:10`     |
| 2   | When they send the message                                                | IMPLEMENTED | `backend/src/api/chat.py:10`, `backend/tests/test_chat_api.py:10`     |
| 3   | Then the system backend receives the raw text of the question.            | IMPLEMENTED | `backend/src/api/chat.py:10`, `backend/tests/test_chat_api.py:11-12`  |
| 4   | And the backend identifies the user's core intent and the key entity.     | IMPLEMENTED | `backend/src/rag/query_parser.py:14-27`, `backend/src/api/chat.py:14`, `backend/tests/test_query_parser.py` |
**Summary:** 4 of 4 acceptance criteria fully implemented.

### Task Completion Validation:
| Task                                                                      | Marked As | Verified As        | Evidence                                                         |
| :------------------------------------------------------------------------ | :-------- | :----------------- | :--------------------------------------------------------------- |
| **Task 1: Design and Implement FastAPI Endpoint**                         | [x]       | VERIFIED COMPLETE  | `backend/src/api/chat.py`, `backend/main.py`                     |
| Subtask 1.1: Create `backend/src/api/chat.py`                             | [x]       | VERIFIED COMPLETE  | `backend/src/api/chat.py` exists                                 |
| Subtask 1.2: Define `POST /chat` endpoint                                 | [x]       | VERIFIED COMPLETE  | `backend/src/api/chat.py:9-12`                                   |
| Subtask 1.3: Integrate router into `backend/main.py`                      | [x]       | VERIFIED COMPLETE  | `backend/main.py:4-5`                                            |
| Subtask 1.4: Implement placeholder response                               | [x]       | VERIFIED COMPLETE  | `backend/src/api/chat.py:14` (returns parsed query)              |
| **Task 2: Implement Intent and Entity Extraction Logic**                  | [x]       | VERIFIED COMPLETE  | `backend/src/rag/query_parser.py`, `backend/src/api/chat.py`     |
| Subtask 2.1: Create `backend/src/rag/query_parser.py`                     | [x]       | VERIFIED COMPLETE  | `backend/src/rag/query_parser.py` exists                         |
| Subtask 2.2: Implement `parse_query` function                             | [x]       | VERIFIED COMPLETE  | `backend/src/rag/query_parser.py:11-28`                          |
| Subtask 2.3: Use keyword matching/regex                                   | [x]       | VERIFIED COMPLETE  | `backend/src/rag/query_parser.py:15-27`                          |
| Subtask 2.4: Define Pydantic model for parsed output                      | [x]       | VERIFIED COMPLETE  | `backend/src/rag/query_parser.py:6-8`                            |
| Subtask 2.5: Integrate `query_parser.py` into `POST /chat`                | [x]       | VERIFIED COMPLETE  | `backend/src/api/chat.py:4, 14`                                  |
| **Task 3: Write Backend Tests (Pytest)**                                  | [x]       | VERIFIED COMPLETE  | `backend/tests/test_chat_api.py`, `backend/tests/test_query_parser.py` |
| Subtask 3.1: Create `backend/tests/test_chat_api.py`                      | [x]       | VERIFIED COMPLETE  | `backend/tests/test_chat_api.py` exists                          |
| Subtask 3.2: Write test for `POST /chat` endpoint                         | [x]       | VERIFIED COMPLETE  | `backend/tests/test_chat_api.py:7-15`                            |
| Subtask 3.3: Create `backend/tests/test_query_parser.py`                  | [x]       | VERIFIED COMPLETE  | `backend/tests/test_query_parser.py` exists                      |
| Subtask 3.4: Write unit tests for `query_parser.py`                       | [x]       | VERIFIED COMPLETE  | `backend/tests/test_query_parser.py:9-20`                        |
**Summary:** 15 of 15 completed tasks verified, 0 questionable, 0 falsely marked complete.

### Test Coverage and Gaps:
*   Unit tests cover intent/entity extraction.
*   Integration test covers the FastAPI endpoint receiving the query and returning parsed data.
*   All tests passed.
*   The `PydanticDeprecatedSince20` warning in `test_knowledge_base_manager.py` is a minor cleanup item for an existing file.

### Architectural Alignment:
*   The implementation aligns with the backend API pattern (REST), AI application (RAG entry point), and project structure outlined in `architecture.md`.

### Security Notes:
*   Input is parsed, not directly executed, reducing injection risks.
*   No sensitive data handling in this story.

### Best-Practices and References:
*   Used FastAPI and Pydantic for robust API and data validation.
*   Implemented Pytest for comprehensive testing.

### Action Items:
**Advisory Notes:**
*   Note: Update `backend/tests/test_knowledge_base_manager.py` to use `model_dump()` instead of `dict()` for Pydantic v2 compatibility. This is a cleanup task for technical debt, not a blocker for this story.

