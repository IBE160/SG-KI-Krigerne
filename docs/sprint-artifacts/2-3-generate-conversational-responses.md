# Story 2.3: Generate Conversational Responses

Status: done

## Story

As a User,
I want to receive answers in a clear and conversational format,
so that the information is easy to understand.

## Acceptance Criteria

1.  **Given** the system has successfully retrieved a piece of information (e.g., "4-hour written exam") from the knowledge base (output of Story 2.2),
2.  **When** the generation component in the backend (`backend/src/rag/`) is invoked with this retrieved information,
3.  **Then** it shall format this information into a clear, natural language sentence (e.g., "The exam format for TDT4140 is a 4-hour written exam.").
4.  **And** the generated conversational response shall be sent back to the UI within 2 seconds.
5.  **And** the backend's `/chat` streaming endpoint (`POST /chat`) shall deliver the response to the frontend using Server-Sent Events (SSE) or streaming HTTP, where each partial response is a JSON chunk (`{ "type": "chunk", "content": "..." }`). A final `{ "type": "done" }` message must be sent to signal completion.
6.  **And** the frontend UI shall display this generated response within the chat history, ensuring it adheres to the "Structured Clarity" design direction for assistant messages (left-aligned, appropriate styling), and displays a typing indicator while receiving the streamed response.

## Tasks / Subtasks

**Core Implementation Tasks:**

1.  **Develop the Generation Component (backend/src/rag/):** (AC: 1, 2, 3)
    *   [ ] Create a new Python module (e.g., `generator.py`) within `backend/src/rag/`.
    *   [ ] Implement a function/class to take structured data (e.g., a dictionary with intent, entity, and retrieved data) as input.
    *   [ ] Using the Gemini API (or a simple templating approach for MVP), generate a natural language sentence from the input.
    *   [ ] Ensure the generated response is conversational and directly answers the implied user question.
    *   [ ] Integrate this generator with the output of the retrieval component (from Story 2.2).

2.  **Implement Streaming API Endpoint (backend/src/api/):** (AC: 5)
    *   [ ] Modify or create a new endpoint in `backend/src/api/` (e.g., `chat_api.py`) to handle the `/chat` route.
    *   [ ] Implement Server-Sent Events (SSE) or streaming HTTP to allow the backend to push partial responses to the frontend.
    *   [ ] Ensure each chunk sent is a JSON object with `type: "chunk"` and `content: "..."`, followed by a final `type: "done"` message.
    *   [ ] Integrate the generation component's output into this streaming mechanism.

3.  **Integrate Streaming Response in Frontend (frontend/src/):** (AC: 6)
    *   [ ] Update the `frontend/src/lib/api-client.ts` to handle streaming responses from the `/chat` endpoint.
    *   [ ] Modify relevant React components in `frontend/src/components/` (e.g., `ChatWindow`, `ChatMessageBubble`) to:
        *   [ ] Render a typing indicator while receiving streamed content.
        *   [ ] Append streamed chunks to the assistant's message in real-time.
        *   [ ] Stop the typing indicator and finalize the message upon receiving the `{ "type": "done" }` signal.
        *   [ ] Ensure messages are displayed according to UX specifications (left-aligned, correct styling).

**Testing Tasks:**

1.  **Unit Tests for Generation Component (backend/tests/):** (AC: 3)
    *   [ ] Write tests for `backend/src/rag/generator.py` to verify:
        *   Correct formatting of various types of retrieved information into natural language sentences.
        *   Handling of edge cases (e.g., empty retrieved data if the retriever is somehow invoked with it).

2.  **Integration Tests for Streaming API (backend/tests/):** (AC: 4, 5)
    *   [ ] Write tests to verify the `/chat` endpoint correctly streams responses.
    *   [ ] Test the format of the streamed JSON chunks (`type`, `content`).
    *   [ ] Verify the endpoint sends the final `{ "type": "done" }` message.
    *   [ ] Ensure the 2-second response time performance criterion is met for typical queries.

3.  **Frontend Integration Tests (frontend/tests/):** (AC: 6)
    *   [ ] Write tests to verify the frontend correctly handles and displays streamed responses.
    *   [ ] Test the display of typing indicators.
    *   [ ] Verify partial messages are appended correctly.
    *   [ ] Test that the message is finalized correctly after receiving the "done" signal.
    *   [ ] Ensure responsiveness and accessibility of the message display.

## Dev Notes

### Architecture patterns and constraints
- The implementation must adhere to the RAG (Retrieval-Augmented Generation) architecture defined in `docs/architecture.md`.
- Data access should be isolated to the `backend/src/db` and `backend/src/rag` modules.
- The generation logic will initially use a simple template but must be designed for easy integration with the Gemini API.

### Project Structure Notes

*   The generation component logic should reside in `backend/src/rag/`.
*   The API endpoint to stream responses will be in `backend/src/api/`.
*   Frontend UI components for displaying messages will be in `frontend/src/components/`.
*   Frontend API client for communication will be in `frontend/src/lib/`.

### Learnings from Previous Story

**From Story 2.2: Implement Knowledge Base Retrieval (Status: done)**

- **New Files Created**: `backend/src/rag/knowledge_base_retriever.py`, `backend/tests/test_knowledge_base_retriever.py`.
- **CRITICAL: Unresolved Review Items from Story 1.3**: The following action items from the review of Story 1.3 are still pending and must be considered in future UI-related stories, as they impact the overall quality and accessibility of the chat interface:
    - [ ] [Medium] Implement robust automated tests for desktop responsiveness
    - [ ] [Medium] Implement robust automated tests for mobile responsiveness
    - [ ] [Medium] Implement robust automated tests for keyboard navigation accessibility
    - [ ] [Medium] Implement robust automated tests for color contrast accessibility
    - [ ] [Medium] Implement robust automated tests for `aria-labels` accessibility

This story builds directly on the outputs of Story 2.2, which handled the retrieval of information from the knowledge base. The primary output of Story 2.2 is a piece of information (e.g., "4-hour written exam") that needs to be formatted conversationally.

**From Story 1.2: Design and Implement the Knowledge Base Schema (Status: done)**

-   **New Files Created**:
    -   `backend/src/models/course.py`: Defines the data structure for course information. This will be crucial for understanding the format of retrieved data to be generated into conversational responses.
    -   `backend/src/db/knowledge_base_manager.py`: Manages interactions with `knowledge_base.json`. This service provides the mechanism for retrieving raw data.
    -   `backend/src/db/knowledge_base.json`: The source of truth for course information.
-   **Warnings for Next**:
    -   "Pydantic Deprecation Warnings: Tests produce deprecation warnings related to Pydantic's `typing.py` (e.g., `backend/venv/Lib/site-packages/pydantic/typing.py:400`). These do not affect current functionality but indicate a future compatibility concern." This should be kept in mind, particularly if Pydantic is used for request/response models in the generation component.
-   **Pending Items**:
    -   "[LOW] Address Pydantic deprecation warnings in `backend/src/models/course.py` (consider upgrading Pydantic or adjusting usage for future Python versions)." This is a low priority but a point of awareness.

### References

-   [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Story-2.3]
-   [Source: docs/sprint-artifacts/2-2-implement-knowledge-base-retrieval.md]
-   [Source: docs/epics.md#Story 2.3: Generate Conversational Responses (MVP)]
-   [Source: docs/prd.md#FR3]
-   [Source: docs/architecture.md#Decision Summary]
-   [Source: docs/architecture.md#API Contracts]
-   [Source: docs/ux-design-specification.md#Core User Experience]
-   [Source: docs/ux-design-specification.md#Custom Component: Chat Message Bubble]
-   [Source: docs/ux-design-specification.md#UX Pattern Decisions]

## Change Log
- **Date:** Wednesday, December 3, 2025
- **Description:** Initial draft created.
- **Date:** Wednesday, December 3, 2025
- **Description:** Addressed validation feedback: added learnings from previous story, added architecture patterns, initialized change log, added AC references to tasks, and added missing citations.

## Dev Agent Record

### Context Reference
- [docs/sprint-artifacts/2-3-generate-conversational-responses.context.xml]

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
