# Story 2.1: Implement Natural Language Query Input

**Epic:** [2 - Core Question Answering](docs/epics.md)
Status: ready-for-dev
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

- [ ] **Task 1: Design and Implement FastAPI Endpoint for Natural Language Query (AC: 1, 2, 3)**
    - [ ] Subtask 1.1: Create a new file `backend/src/api/chat.py` to house the chat endpoint.
    - [ ] Subtask 1.2: Define a `POST /chat` endpoint in `backend/src/api/chat.py` that accepts a JSON payload with a `query` string (e.g., `{"query": "what is the exam format for TDT4140?"}`).
    - [ ] Subtask 1.3: Integrate the new `chat` router into `backend/main.py`.
    - [ ] Subtask 1.4: Implement a basic placeholder response for the endpoint (e.g., echoing the received query) to verify connectivity.
- [ ] **Task 2: Implement Intent and Entity Extraction Logic (AC: 4)**
    - [ ] Subtask 2.1: Create a new file `backend/src/rag/query_parser.py` for query parsing logic.
    - [ ] Subtask 2.2: Implement a function in `query_parser.py` that takes a natural language `query` string as input.
    - [ ] Subtask 2.3: Use simple keyword matching or regex to identify core intent (e.g., `get_exam_format`, `get_learning_outcomes`, `get_mandatory_assignments`) and extract relevant entities (e.g., `course_code: TDT4140`).
    - [ ] Subtask 2.4: Define a clear output structure for the parsed intent and entities (e.g., a Pydantic model).
    - [ ] Subtask 2.5: Integrate the `query_parser.py` into the `POST /chat` endpoint to process the incoming query.
- [ ] **Task 3: Write Backend Tests (Pytest)**
    - [ ] Subtask 3.1: Create a test file `backend/tests/test_chat_api.py`.
    - [ ] Subtask 3.2: Write a test for the `POST /chat` endpoint to ensure it receives a query and returns a placeholder response. (AC: 1, 2, 3)
    - [ ] Subtask 3.3: Create a test file `backend/tests/test_query_parser.py`.
    - [ ] Subtask 3.4: Write unit tests for `query_parser.py` to verify correct intent and entity extraction for various natural language queries. (AC: 4)
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
### Completion Notes List
### File List
- `backend/src/api/chat.py`
- `backend/src/rag/query_parser.py`
- `backend/tests/test_chat_api.py`
- `backend/tests/test_query_parser.py`
- `backend/main.py` (modified)

## Change Log
- **Date:** December 3, 2025
- **Description:** Initial draft of Story 2.1 created from `epics.md`, `prd.md`, `architecture.md`, and `ux-design-specification.md`. Lessons learned from Story 1.4 incorporated.
