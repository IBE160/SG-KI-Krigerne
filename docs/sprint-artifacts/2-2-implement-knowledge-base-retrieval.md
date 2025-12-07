# Story 2.2: Implement Knowledge Base Retrieval

**Epic:** [2 - Core Question Answering](docs/epics.md)
Status: ready-for-dev
**Points:** (TBD - estimate during sprint planning)
**Author:** BIP

## User Story

As a **System**,
I want **to search the structured knowledge base for specific information based on a parsed query**,
So that **I can provide the generation component with the context needed to answer a user's question**.

## Acceptance Criteria

*(Source: [docs/sprint-artifacts/tech-spec-epic-2.md#Story-2.2](docs/sprint-artifacts/tech-spec-epic-2.md))*

1.  **Given** a parsed intent (e.g., `get_exam_format`) and entity (e.g., `course_code: TDT4140`),
2.  **When** the retrieval component is invoked,
3.  **Then** it searches the `knowledge_base.json` (or PostgreSQL equivalent) for the matching course.
4.  **And** it extracts the specific information requested (e.g., the value of the `exam_format` field for `TDT4140`).
5.  **And** if no matching course or information is found, it returns a "not found" signal.

## Tasks / Subtasks

- [ ] **Task 1: Implement Knowledge Base Retrieval Logic (AC: 1, 2, 3, 4, 5)**
    - [ ] Subtask 1.1: Create a new file `backend/src/rag/knowledge_base_retriever.py`.
    - [ ] Subtask 1.2: Implement a function in `knowledge_base_retriever.py` that takes a parsed query (intent and entity) as input.
    - [ ] Subtask 1.3: The function should connect to the `knowledge_base.json` (or PostgreSQL DB).
    - [ ] Subtask 1.4: Implement logic to find the course matching the entity (`course_code`).
    - [ ] Subtask 1.5: Implement logic to extract the specific field based on the intent.
    - [ ] Subtask 1.6: Return the extracted information or a "not found" signal.
- [ ] **Task 2: Integrate Retriever with Chat API (AC: 1, 2)**
    - [ ] Subtask 2.1: In `backend/src/api/chat.py`, import and call the knowledge base retriever after parsing the query.
    - [ ] Subtask 2.2: Pass the parsed query to the retriever.
    - [ ] Subtask 2.3: For now, return the retrieved information (or "not found" signal) as a placeholder response.
- [ ] **Task 3: Write Backend Tests (Pytest)**
    - [ ] Subtask 3.1: Create `backend/tests/test_knowledge_base_retriever.py`.
    - [ ] Subtask 3.2: Write a test for successful course and information retrieval. (AC: 3, 4)
    - [ ] Subtask 3.3: Write a test to verify "not found" signal for a non-existent course. (AC: 5)
    - [ ] Subtask 3.4: Write a test to verify "not found" signal for a non-existent field. (AC: 5)
    - [ ] Subtask 3.5: Write an integration test to verify the retriever is called from the chat API. (AC: 1, 2)

## Dev Notes

### Learnings from Previous Story
**From Story 2.1: Implement Natural Language Query Input (Status: done)**

- **New Files Created**: `backend/src/api/chat.py`, `backend/src/rag/query_parser.py`, `backend/tests/test_chat_api.py`, `backend/tests/test_query_parser.py`. The `query_parser` is the direct input to this story.
- **Modified Files**: `backend/main.py`, `backend/requirements.txt`.
- **New Services**: A `/chat` endpoint now exists in FastAPI, and a query parser can extract intent and entities. This story will build upon the parsed query.
- **Technical Debt**: A Pydantic deprecation warning (`.dict()` vs `.model_dump()`) exists in `test_knowledge_base_manager.py`. While not part of this story, it's a known issue.
- **CRITICAL: Unresolved Review Items from Story 1.3**: The following action items from the review of Story 1.3 are still pending and must be considered in future UI-related stories, as they impact the overall quality and accessibility of the chat interface:
    - [ ] [Medium] Implement robust automated tests for desktop responsiveness
    - [ ] [Medium] Implement robust automated tests for mobile responsiveness
    - [ ] [Medium] Implement robust automated tests for keyboard navigation accessibility
    - [ ] [Medium] Implement robust automated tests for color contrast accessibility
    - [ ] [Medium] Implement robust automated tests for `aria-labels` accessibility

[Source: docs/sprint-artifacts/2-1-implement-natural-language-query-input.md#Dev-Agent-Record]

### Architecture Patterns and Constraints
- The implementation must adhere to the RAG (Retrieval-Augmented Generation) architecture defined in `docs/architecture.md`.
- Data access should be isolated to the `backend/src/db` and `backend/src/rag` modules.
- The retrieval logic will initially target a JSON file but must be designed for easy migration to PostgreSQL as per the architecture decision.

### Project Structure Notes
- All backend implementation will be within the `backend/` directory.
- This story will create `backend/src/rag/knowledge_base_retriever.py` and `backend/tests/test_knowledge_base_retriever.py`.
- It will modify `backend/src/api/chat.py` to integrate the new retriever.

### References
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Story-2.2]
- [Source: docs/architecture.md#Data-Persistence]
- [Source: docs/epics.md#Story-2.2-Implement-Knowledge-Base-Retrieval-(MVP)]

## Change Log
- **Date:** Wednesday, December 3, 2025
- **Description:** Initial draft created.
- **Date:** Wednesday, December 3, 2025
- **Description:** Addressed validation feedback: added missing "CRITICAL: Unresolved Review Items from Story 1.3" to learnings, refactored testing tasks for better AC coverage, added "Architecture Patterns and Constraints" section, updated tech spec citation, and initialized the change log.

## Dev Agent Record

### Context Reference
- `docs/sprint-artifacts/2-2-implement-knowledge-base-retrieval.context.xml`

### Agent Model Used
{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
