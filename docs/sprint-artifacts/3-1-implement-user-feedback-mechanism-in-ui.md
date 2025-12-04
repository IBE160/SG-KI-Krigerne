# Story 3.1: Implement User Feedback Mechanism in UI

Status: ready-for-dev

## Story

As a User,
I want to easily provide feedback on the chatbot's answers,
so that the system can be improved.

## Acceptance Criteria

1.  **AC 3.1.1:** Given a chatbot response is displayed, when the response is rendered, then "thumbs up" (👍) and "thumbs down" (👎) icons are displayed next to the response.
2.  **AC 3.1.2:** Given "thumbs up" or "thumbs down" icons are displayed, when a user clicks either icon, then a feedback signal is sent to the backend.
3.  **AC 3.1.3:** Given feedback has been sent, when the icons are displayed, then they change state (e.g., become greyed out or show a "Thank you" message) to indicate feedback was received.

## Tasks / Subtasks

**Core Implementation Tasks:**

1.  **Frontend: Implement FeedbackDisplay Component (`frontend/src/components/FeedbackDisplay.tsx`)**: (AC: 3.1.1, 3.1.2, 3.1.3)
    *   [ ] Render 👍 and 👎 icons next to each bot message.
    *   [ ] Implement click handlers for both icons to capture rating (1 or -1), query, and response.
    *   [ ] Integrate with `ApiClient` to send feedback to `POST /feedback`.
    *   [ ] Update UI state to reflect feedback submission (e.g., disable icons, show "Thank you").
2.  **Frontend: Extend ApiClient (`frontend/src/lib/api-client.ts`)**: (AC: 3.1.2)
    *   [ ] Add `sendFeedback(feedbackData: FeedbackData)` method to make POST request to `/feedback` endpoint.
3.  **Backend: Create FeedbackAPI Endpoint (`backend/src/api/feedback.py`)**: (AC: 3.1.2)
    *   [ ] Define `POST /feedback` endpoint.
    *   [ ] Implement request body validation using `FeedbackCreate` Pydantic model.
    *   [ ] Call `FeedbackService` to process and persist feedback (actual persistence handled by Story 3.2).

**Testing Tasks:**

1.  **Frontend Unit Tests (`frontend/tests/FeedbackDisplay.test.tsx` - TBD naming)**: (AC: 3.1.1, 3.1.3)
    *   [ ] Test rendering of feedback icons.
    *   [ ] Test UI state changes after feedback (icons disabled/thank you message).
    *   [ ] Mock `ApiClient.sendFeedback` to verify calls.
2.  **Backend Unit Tests (`backend/tests/test_feedback_api.py`)**: (AC: 3.1.2)
    *   [ ] Test `POST /feedback` endpoint request validation.
    *   [ ] Mock `FeedbackService` to verify correct calls.
3.  **Frontend Integration Test**: (AC: 3.1.1, 3.1.2, 3.1.3)
    *   [ ] Simulate a full feedback submission flow from UI click to backend call (mocking backend response).
    *   [ ] Verify end-to-end user experience.
4.  **Accessibility Testing for FeedbackDisplay (Automated/Manual)**: (AC: 3.1.1, 3.1.3, and addressing previous story learnings)
    *   [ ] Verify keyboard navigation for feedback icons.
    *   [ ] Check for proper `aria-labels` on icons.
    *   [ ] Ensure sufficient color contrast for feedback elements.
    *   [ ] Test responsiveness of feedback elements on desktop/mobile.

## Dev Notes

### Architecture patterns and constraints
- This story reinforces the established system architecture leveraging frontend (Vite + React SPA with `shadcn/ui`, Tailwind CSS) and backend (Python REST API with FastAPI) components.
- Specific attention to non-functional requirements like performance (fast UI update, quick backend response for feedback signal), security (no PII in data sent to backend, endpoint protection), reliability (high availability of feedback mechanism, graceful degradation), and observability (logging feedback events).

### Source tree components to touch
- `frontend/src/components/FeedbackDisplay.tsx` (new component)
- `frontend/src/lib/api-client.ts` (modification)
- `backend/src/api/feedback.py` (new endpoint file - will implement the `POST /feedback` route)
- `backend/src/services/feedback_service.py` (new service file - will implement the feedback processing logic, mocked for this story's backend unit tests)
- `backend/src/models/feedback.py` (new data models file - Pydantic models for feedback)

### Testing standards summary
- Unit tests for Frontend (`FeedbackDisplay` component) using Jest/Vitest, mocking API calls.
- Unit tests for Backend (`FeedbackAPI`, `FeedbackService` - mocked persistence) using Pytest.
- Integration tests for Frontend-Backend API communication flow.
- Accessibility testing (keyboard navigation, `aria-labels`, contrast, responsiveness) for the UI components.

### Project Structure Notes
- Alignment with unified project structure: New files and modifications adhere to the established conventions for `frontend/src/components`, `frontend/src/lib`, `backend/src/api`, `backend/src/services`, `backend/src/models`.
- Detected conflicts or variances: None. New files align with existing structure.

### Learnings from Previous Story

**From Story 2.4: Handle "I Don't Know" Scenarios (Status: done)**

-   **Architectural patterns**: Reinforces AI Safety (preventing LLM hallucination), hardcoded template for "I don't know" responses. (Indirectly relevant for this story in terms of maintaining overall system integrity).
-   **Technical Debt**: Pydantic deprecation warnings in `backend/tests/test_knowledge_base_manager.py` (low severity advisory) - `model_dump()` recommended. (Not directly relevant to this story, but noted for overall project health).
-   **Warnings/Recommendations (Accessibility for UI stories)**: The following accessibility-related automated tests are still pending from Story 1.3 and should be addressed or considered for this UI-heavy story (Story 3.1) to ensure comprehensive accessibility:
    *   [Medium] Implement robust automated tests for desktop responsiveness.
    *   [Medium] Implement robust automated tests for mobile responsiveness.
    *   [Medium] Implement robust automated tests for keyboard navigation accessibility.
    *   [Medium] Implement robust automated tests for color contrast accessibility.
    *   [Medium] Implement robust automated tests for `aria-labels` accessibility.

### References
- [Source: docs/prd.md#FR5]
- [Source: docs/epics.md#Story 3.1: Implement User Feedback Mechanism in UI (MVP)]
- [Source: docs/sprint-artifacts/tech-spec-epic-3.md#Detailed-Design]
- [Source: docs/sprint-artifacts/tech-spec-epic-3.md#Non-Functional-Requirements]
- [Source: docs/sprint-artifacts/tech-spec-epic-3.md#Acceptance-Criteria-(Authoritative)]
- [Source: docs/sprint-artifacts/tech-spec-epic-3.md#Test-Strategy-Summary]
- [Source: docs/sprint-artifacts/2-4-handle-i-dont-know-scenarios.md#Dev-Agent-Record]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/3-1-implement-user-feedback-mechanism-in-ui.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List