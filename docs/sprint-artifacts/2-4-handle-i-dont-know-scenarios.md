# Story 2.4: Handle "I Don't Know" Scenarios

Status: ready-for-dev

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
    *   [ ] Modify the generation component (`generator.py`) to accept the "not found" signal from the retrieval component.
    *   [ ] Implement logic to, upon receiving the "not found" signal, bypass the Gemini API and return a predefined, polite "I don't know" message.
    *   [ ] Ensure this message is formatted as a standard conversational response.

2.  **Integrate "Not Found" Logic into Chat Service (backend/src/api/):** (from Story 2.3)
    *   [ ] Ensure the main chat service orchestrator correctly passes the "not found" signal from the retriever to the generator.
    *   [ ] Verify that the streaming endpoint (`chat_api.py`) correctly handles and streams the "I don't know" response generated.

**Testing Tasks:**

1.  **Unit Tests for "I Don't Know" Logic (backend/tests/):** (AC: 3)
    *   [ ] Write unit tests for `backend/src/rag/generator.py` to verify that it produces the correct "I don't know" message when the "not found" signal is provided.
    *   [ ] Test that it does NOT call the Gemini API in this scenario.

2.  **Integration Tests for "I Don't Know" Flow (backend/tests/):** (AC: 4)
    *   [ ] Write an integration test for the `/chat` endpoint that simulates the retriever returning "not found".
    *   [ ] Verify that the streamed response from the API is the expected "I don't know" message.

3.  **Frontend Integration Tests (frontend/tests/):** (AC: 4)
    *   [ ] Write a test to ensure the frontend correctly displays the "I don't know" message received from the backend.
    *   [ ] Verify the message is styled correctly as an assistant message.

4.  **Streaming Endpoint Verification (backend/tests/):** (from Story 2.3)
    *   [ ] Write a test to confirm the "I don't know" response is delivered in the correct streaming JSON format (`{ "type": "chunk", "content": "..." }` followed by `{ "type": "done" }`).

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
    - [ ] [Medium] Implement robust automated tests for keyboard navigation accessibility
    - [ ] [Medium] Implement robust automated tests for color contrast accessibility
    - [ ] [Medium] Implement robust automated tests for `aria-labels` accessibility

### References

-   [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Story-2.4]
-   [Source: docs/epics.md#Story 2.4: Handle "I Don't Know" Scenarios (MVP)]
-   [Source: docs/prd.md#FR10]
-   [Source: docs/architecture.md#AI Safety]

## Change Log
- **Date:** Wednesday, December 3, 2025
- **Description:** Initial draft created.

## Dev Agent Record

### Context Reference
- [docs/sprint-artifacts/2-4-handle-i-dont-know-scenarios.context.xml]

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
    *   [ ] Modify the generation component (`generator.py`) to accept the "not found" signal from the retrieval component.
    *   [ ] Implement logic to, upon receiving the "not found" signal, bypass the Gemini API and return a predefined, polite "I don't know" message.
    *   [ ] Ensure this message is formatted as a standard conversational response.

2.  **Integrate "Not Found" Logic into Chat Service (backend/src/api/):** (from Story 2.3)
    *   [ ] Ensure the main chat service orchestrator correctly passes the "not found" signal from the retriever to the generator.
    *   [ ] Verify that the streaming endpoint (`chat_api.py`) correctly handles and streams the "I don't know" response generated.

**Testing Tasks:**

1.  **Unit Tests for "I Don't Know" Logic (backend/tests/):** (AC: 3)
    *   [ ] Write unit tests for `backend/src/rag/generator.py` to verify that it produces the correct "I don't know" message when the "not found" signal is provided.
    *   [ ] Test that it does NOT call the Gemini API in this scenario.

2.  **Integration Tests for "I Don't Know" Flow (backend/tests/):** (AC: 4)
    *   [ ] Write an integration test for the `/chat` endpoint that simulates the retriever returning "not found".
    *   [ ] Verify that the streamed response from the API is the expected "I don't know" message.

3.  **Frontend Integration Tests (frontend/tests/):** (AC: 4)
    *   [ ] Write a test to ensure the frontend correctly displays the "I don't know" message received from the backend.
    *   [ ] Verify the message is styled correctly as an assistant message.

4.  **Streaming Endpoint Verification (backend/tests/):** (from Story 2.3)
    *   [ ] Write a test to confirm the "I don't know" response is delivered in the correct streaming JSON format (`{ "type": "chunk", "content": "..." }` followed by `{ "type": "done" }`).

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
    - [ ] [Medium] Implement robust automated tests for keyboard navigation accessibility
    - [ ] [Medium] Implement robust automated tests for color contrast accessibility
    - [ ] [Medium] Implement robust automated tests for `aria-labels` accessibility

### References

-   [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Story-2.4]
-   [Source: docs/epics.md#Story 2.4: Handle "I Don't Know" Scenarios (MVP)]
-   [Source: docs/prd.md#FR10]
-   [Source: docs/architecture.md#AI Safety]

## Change Log
- **Date:** Wednesday, December 3, 2025
- **Description:** Initial draft created.
