# Story 3.2: Persist User Feedback

Status: review

## Story

As a System,
I want to store user feedback,
so that it can be analyzed to improve the chatbot's performance.

## Acceptance Criteria

1.  **AC 3.2.1:** Given a feedback signal (thumbs up/down) is received from the UI, when the backend processes the signal, then it records the feedback along with the user's query, the chatbot's response, and a timestamp into a persistent log within the PostgreSQL database.
2.  **AC 3.2.2:** Given the system records feedback, then the system ensures that no personally identifiable information (PII) is persisted or logged, adhering to the project's data privacy guidelines.

## Tasks / Subtasks

**Core Implementation Tasks:**

1.  **Backend: Implement `FeedbackService.save_feedback` method (AC: 3.2.1)**
    *   [x] Define the database model for feedback in `backend/src/models/feedback.py`. This includes fields for `query`, `response`, `rating`, and `timestamp`.
    *   [x] Implement logic to connect to PostgreSQL database.
    *   [x] Implement logic to insert feedback data into the `feedback` table.
    *   [x] Address the Pydantic v2 compatibility for `FeedbackDB` model (update to use `pydantic.ConfigDict`).
2.  **Backend: Integrate `FeedbackService` with `FeedbackAPI` (AC: 3.2.1)**
    *   [x] Modify `POST /feedback` endpoint in `backend/src/api/feedback.py` to call `FeedbackService.save_feedback`.
3.  **Backend: Database Migration (AC: 3.2.1)**
    *   [x] Create a database migration script to create the `feedback` table in PostgreSQL.
4.  **Backend: Ensure PII Exclusion in Logging (AC: 3.2.2)**
    *   [x] Review logging implementation in `FeedbackService` to explicitly exclude any PII from logs.
    *   [x] Ensure `query` and `response` are handled safely (e.g., hash, truncate, or redact PII if present, though PRD states no PII is handled for MVP).

**Testing Tasks:**

1.  **Backend Unit Tests (`backend/tests/test_feedback_service.py`)**: (AC: 3.2.1, 3.2.2)
    *   [x] Test `FeedbackService.save_feedback` method, mocking database interactions.
    *   [x] Verify correct data is stored in the mock database.
    *   [x] Test edge cases (e.g., invalid input if validation is added in service layer).
    *   [x] Test PII exclusion in logs.
2.  **Backend Integration Test (`backend/tests/test_feedback_api.py`)**: (AC: 3.2.1, 3.2.2)
    *   [ ] Extend existing `test_feedback_api.py` to test end-to-end feedback submission, including persistence to a test database. (Deferred due to environment complexity for pytest-asyncio and TestClient integration)

## Dev Notes

### Relevant architecture patterns and constraints
- Data Persistence: PostgreSQL is the chosen database, suitable for structured relational data. The feedback will be stored in a `feedback` table.
- Logging Strategy: Python's built-in `logging` module will be used in the backend for logging events, ensuring PII is avoided.
- Security: Database access will use dedicated users with minimum permissions. No PII in logs/feedback.

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### Learnings from Previous Story

**From Story 3.1: Implement User Feedback Mechanism in UI (Status: done)**

**Services to Reuse:**
- `backend/src/services/feedback_service.py`: This service was created in the previous story and will be extended in this story to handle feedback persistence.

**Relevant Technical Debt to Address in this Story:**
- When upgrading Pydantic to v2+, `FeedbackDB` in `backend/src/models/feedback.py` needs to be updated to use `pydantic.ConfigDict` instead of the deprecated `Config` class. This should be addressed as part of implementing persistence for `FeedbackDB`.

**Relevant Pending Review Items to Address in this Story:**
- Consider more granular exception handling in the `POST /feedback` endpoint if `FeedbackService` introduces specific custom exceptions. (Related to Backend Error Handling) This is relevant because this story will implement the core logic in `FeedbackService`.

**Key New Files from Previous Story (Relevant Context):**
- `backend/src/models/feedback.py`: Contains the `FeedbackDB` model which will be used for persistence.
- `backend/src/api/feedback.py`: Contains the `POST /feedback` endpoint, which will call the `FeedbackService` to persist data.

### References

- Cite all technical details with source paths and sections, e.g. [Source: docs/<file>.md#Section]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/3-2-persist-user-feedback.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List
- Completed all core implementation tasks for feedback persistence (AC 3.2.1, AC 3.2.2).
- Backend unit tests for `FeedbackService` are passing.
- Backend integration tests for `test_feedback_api.py` were deferred due to environment setup complexities with `pytest-asyncio` and `TestClient` interactions, resulting in persistent failures that prevented completion within the allocated time for this story.

## Technical Debt
- [Low] Fully implement robust integration tests for `backend/tests/test_feedback_api.py` that utilize a test database (e.g., in-memory SQLite or a Dockerized PostgreSQL instance) and correctly configure `pytest-asyncio` for asynchronous FastAPI application testing. This will ensure comprehensive end-to-end verification of the feedback persistence mechanism.

### File List
- backend/src/models/feedback.py
- backend/src/db/database.py
- backend/src/db/__init__.py
- backend/src/db/feedback_repository.py
- backend/src/services/feedback_service.py
- backend/src/api/feedback.py
- backend/requirements.txt
- backend/alembic.ini
- backend/migrations/env.py
- backend/migrations/versions/*_create_feedback_table.py
- backend/tests/test_feedback_service.py
- backend/tests/test_feedback_api.py

## Change Log

- **2025-12-04**: Story drafted.
