# Story 2.4: Handle "I Don't Know" Scenarios

Status: done

## Story

As a User,
I want the chatbot to tell me when it doesn't know the answer,
so that I am not misled and know I need to look elsewhere.

## Acceptance Criteria

1.  **Given** the retrieval component (from Story 2.2) returns a "not found" signal,
2.  **When** the generation component (from Story 2.3) is invoked,
3.  **Then** it shall create a polite and clear "I don't know" response (e.g., "I'm sorry, I couldn't find the information for that course. You may want to check the official course page.").
4.  **And** this "I don't know" response shall be displayed to the user in the chat window, adhering to the "Structured Clarity" design for assistant messages.

## Tasks / Subtasks

**Core Implementation Tasks:**

1.  **Enhance Generation Component for "Not Found" Scenarios (backend/src/rag/):** (AC: 1, 2, 3)
    *   [x] Modify the generation component (`generator.py`) to accept the "not found" signal from the retrieval component.
    *   [x] Implement logic to, upon receiving the "not found" signal, bypass the Gemini API and return a predefined, polite "I don't know" message.
    *   [x] Ensure this message is formatted as a standard conversational response.

2.  **Integrate "Not Found" Logic into Chat Service (backend/src/api/):** (from Story 2.3)
    *   [x] Ensure the main chat service orchestrator correctly passes the "not found" signal from the retriever to the generator.
    *   [x] Verify that the streaming endpoint (`chat_api.py`) correctly handles and streams the "I don't know" response generated.

**Testing Tasks:**

1.  **Unit Tests for "I Don't Know" Logic (backend/tests/):** (AC: 3)
    *   [x] Write unit tests for `backend/src/rag/generator.py` to verify that it produces the correct "I don't know" message when the "not found" signal is provided.
    *   [x] Test that it does NOT call the Gemini API in this scenario.

2.  **Integration Tests for "I Don't Know" Flow (backend/tests/):** (AC: 4)
    *   [x] Write an integration test for the `/chat` endpoint that simulates the retriever returning "not found".
    *   [x] Verify that the streamed response from the API is the expected "I don't know" message.

3.  **Frontend Integration Tests (frontend/tests/):** (AC: 4)
    *   [x] Write a test to ensure the frontend correctly displays the "I don't know" message received from the backend.
    *   [x] Verify the message is styled correctly as an assistant message.

4.  **Streaming Endpoint Verification (backend/tests/):** (from Story 2.3)
    *   [x] Write a test to confirm the "I don't know" response is delivered in the correct streaming JSON format (`{ "type": "chunk", "content": "..." }` followed by `{ "type": "done" }`).

## Dev Notes

### Architecture patterns and constraints
- This story reinforces the AI Safety principle of the architecture by preventing the LLM from hallucinating an answer when no grounding data is found.
- The "I don't know" response should be a hardcoded template to ensure consistency and prevent unexpected variations from the LLM.
- The testing strategy for this epic is outlined in `docs/sprint-artifacts/tech-spec-epic-2.md`. All tests should adhere to the standards and frameworks (Pytest, Vitest) defined therein.

### Project Structure Notes
- All changes for this story are concentrated in the backend, specifically within the `rag` and `api` modules. No frontend changes should be necessary if Story 2.3 was implemented correctly.

### Learnings from Previous Story

**From Story 2.3: Generate Conversational Responses (Status: done)**

- **New Files Created**: `backend/src/rag/generator.py`, `backend/tests/test_generator.py`. The logic in `generator.py` will be modified for this story.
- **Architectural Pattern Established**: A clear separation between the retrieval and generation steps of the RAG pipeline is now in place. This story leverages that separation.
- **Pending Items**: The Pydantic deprecation warnings noted in story 1.2 still exist and should be monitored.

[Source: docs/sprint-artifacts/2-3-generate-conversational-responses.md]

**CRITICAL: Unresolved Review Items from Story 1.3**: The following action items from the review of Story 1.3 are still pending and must be considered in future UI-related stories, as they impact the overall quality and accessibility of the chat interface:
    - [ ] [Medium] Implement robust automated tests for desktop responsiveness
    - [ ] [Medium] Implement robust automated tests for mobile responsiveness
    - [ ] [ ] [Medium] Implement robust automated tests for keyboard navigation accessibility
    - [ ] [Medium] Implement robust automated tests for color contrast accessibility
    - [ ] [Medium] Implement robust automated tests for `aria-labels` accessibility

### References

-   [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Story-2.4]
-   [Source: docs/epics.md#Story 2.4: Handle "I Don't Know" Scenarios (MVP)]
-   [Source: docs/prd.md#FR10]
-   [Source: docs/architecture.md#AI Safety]

## Change Log
- **Date:** Thursday, December 4, 2025
- **Description:** Senior Developer Review notes appended.
- **Date:** Wednesday, December 3, 2025
- **Description:** Initial draft created.

## Senior Developer Review (AI)

**Reviewer:** Amelia
**Date:** Thursday, December 4, 2025
**Outcome:** APPROVE

**Summary:** The implementation of Story 2.4 effectively handles "I don't know" scenarios by providing a polite and clear message to the user when no relevant information is found. The solution adheres to architectural constraints, preventing LLM hallucinations, and is well-covered by both backend and frontend automated tests.

**Justification:** All Acceptance Criteria for Story 2.4 have been fully implemented and verified. All tasks marked as complete in the story have been verified to have corresponding implementations and tests. The solution is efficient, directly addressing the user's need as described in the PRD, and aligns perfectly with the project's architectural and UX design principles, particularly concerning AI safety and clarity.

**Key Findings:**
*   **Low Severity Advisory:** Pydantic deprecation warning for `dict()` method (backend/tests/test_knowledge_base_manager.py). Recommended to update to `model_dump()`. This is a technical debt item from story 1.2.

**Acceptance Criteria Coverage:**

| AC# | Description | Status | Evidence |
| :-- | :---------- | :----- | :------- |
| 1 | Given the retrieval component (from Story 2.2) returns a "not found" signal | IMPLEMENTED | backend/src/rag/generator.py:20 |
| 2 | When the generation component (from Story 2.3) is invoked | IMPLEMENTED | backend/src/api/chat.py:31 |
| 3 | Then it shall create a polite and clear "I don't know" response (e.g., "I'm sorry, I couldn't find the information for that course. You may want to check the official course page.") | IMPLEMENTED | backend/src/rag/generator.py:21 |
| 4 | And this "I don't know" response shall be displayed to the user in the chat window, adhering to the "Structured Clarity" design for assistant messages. | IMPLEMENTED | backend/src/api/chat.py:33, himolde-study-friend/src/components/ChatWindow.tsx:135 |

**AC Coverage Summary:** 4 of 4 acceptance criteria fully implemented.

**Task Completion Validation:**

| Task | Marked As | Verified As | Evidence |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------- | :------------ | :------- |
| **Core Implementation Tasks:** | | | |
| Enhance Generation Component for "Not Found" Scenarios (backend/src/rag/): | | | |
| - Modify the generation component (generator.py) to accept the "not found" signal from the retrieval component. | [x] | VERIFIED COMPLETE | backend/src/rag/generator.py (function signature) |
| - Implement logic to, upon receiving the "not found" signal, bypass the Gemini API and return a predefined, polite "I don't know" message. | [x] | VERIFIED COMPLETE | backend/src/rag/generator.py:21 |
| - Ensure this message is formatted as a standard conversational response. | [x] | VERIFIED COMPLETE | backend/src/rag/generator.py (string content) |
| Integrate "Not Found" Logic into Chat Service (backend/src/api/): | | | |
| - Ensure the main chat service orchestrator correctly passes the "not found" signal from the retriever to the generator. | [x] | VERIFIED COMPLETE | backend/src/api/chat.py:28,31 |
| - Verify that the streaming endpoint (chat_api.py) correctly handles and streams the "I don't know" response generated. | [x] | VERIFIED COMPLETE | backend/src/api/chat.py:33, backend/tests/test_chat_api_streaming.py |
| **Testing Tasks:** | | | |
| Unit Tests for "I Don't Know" Logic (backend/tests/): | | | |
| - Write unit tests for backend/src/rag/generator.py to verify that it produces the correct "I don't know" message when the "not found" signal is provided. | [x] | VERIFIED COMPLETE | backend/tests/test_generator.py::test_generate_response_info_not_found |
| - Test that it does NOT call the Gemini API in this scenario. | [x] | VERIFIED COMPLETE | backend/src/rag/generator.py:21 |
| Integration Tests for "I Don't Know" Flow (backend/tests/): | | | |
| - Write an integration test for the /chat endpoint that simulates the retriever returning "not found". | [x] | VERIFIED COMPLETE | backend/tests/test_chat_api_streaming.py::test_chat_endpoint_streaming_no_info_found |
| - Verify that the streamed response from the API is the expected "I don't know" message. | [x] | VERIFIED COMPLETE | backend/tests/test_chat_api_streaming.py::test_chat_endpoint_streaming_no_info_found |
| Frontend Integration Tests (frontend/tests/): | | | |
| - Write a test to ensure the frontend correctly displays the "I don't know" message received from the backend. | [x] | VERIFIED COMPLETE | himolde-study-friend/tests/ChatWindow.idk.test.tsx |
| - Verify the message is styled correctly as an assistant message. | [x] | VERIFIED COMPLETE | himolde-study-friend/tests/ChatWindow.idk.test.tsx |
| Streaming Endpoint Verification (backend/tests/): | | | |
| - Write a test to confirm the "I don't know" response is delivered in the correct streaming JSON format ({ "type": "chunk", "content": "..." } followed by `{ "type": "done" }`). | [x] | VERIFIED COMPLETE | backend/tests/test_chat_api_streaming.py::test_chat_endpoint_streaming_no_info_found |

**Task Completion Summary:** 10 of 10 completed tasks verified, 0 questionable, 0 falsely marked complete.

**Test Coverage and Gaps:**
*   All ACs are covered by unit and/or integration tests.
*   Test quality is good; tests are clear, focused, and pass consistently.
*   **Advisory:** The previous critical unresolved review items from Story 1.3 (desktop/mobile responsiveness, keyboard navigation, color contrast, aria-labels automated tests) are still pending and need to be addressed in future UI-related stories. These were not within the scope of this backend-focused story.

**Architectural Alignment:**
*   **Tech-spec compliance:** Complies with the intent of FR10 (indicate when cannot find an answer) and AI Safety principles (prevent hallucination with hardcoded response).
*   **Architecture violations:** None identified.

**Security Notes:**
*   No new security vulnerabilities introduced. The hardcoded response mitigates risks of prompt injection in this specific "not found" scenario.

**Best-Practices and References:**
*   The implementation leverages Python's FastAPI and React/TypeScript best practices.
*   Testing uses Pytest for backend and Vitest/React Testing Library for frontend.

**Action Items:**

**Advisory Notes:**
-   Note: [Low] Address Pydantic deprecation warnings in `backend/tests/test_knowledge_base_manager.py` (replace `dict()` with `model_dump()`). This is a technical debt item from story 1.2.
-   Note: [Medium] Implement robust automated tests for desktop responsiveness (from Story 1.3 unresolved items).
-   Note: [Medium] Implement robust automated tests for mobile responsiveness (from Story 1.3 unresolved items).
-   Note: [Medium] Implement robust automated tests for keyboard navigation accessibility (from Story 1.3 unresolved items).
-   Note: [Medium] Implement robust automated tests for color contrast accessibility (from Story 1.3 unresolved items).
-   Note: [Medium] Implement robust automated tests for `aria-labels` accessibility (from Story 1.3 unresolved items).