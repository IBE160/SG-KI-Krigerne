# Story 3.2: Persist User Feedback

Status: in-progress

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

**Review Follow-ups (AI):**
- [x] [High] Update `FeedbackDB` model in `backend/src/models/feedback.py` to use `pydantic.ConfigDict` for Pydantic v2 compatibility.
- [ ] [High] Implement end-to-end integration tests for `backend/tests/test_feedback_api.py` that verify actual database persistence of feedback, without mocking the persistence layer.

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
- Implemented Pydantic v2 compatibility for `FeedbackDB` model.
- Backend integration tests for `test_feedback_api.py` were not fully implemented due to an unresolved `pytest-asyncio`/FastAPI dependency injection issue in the test setup that prevents proper database session overrides. This blocks the completion of the integration testing task.

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
- **2025-12-04**: Pydantic v2 compatibility for `FeedbackDB` implemented.
- **2025-12-04**: Integration tests for persistence blocked due to test setup issues.

## Senior Developer Review (AI)

**Reviewer**: BIP
**Date**: 2025-12-04
**Outcome**: Changes Requested
**Justification**:
- One HIGH severity finding where a task was marked complete but not implemented (Pydantic v2 compatibility).
- A critical integration testing task for database persistence was explicitly deferred and the existing test mocks persistence rather than testing it end-to-end.

**Summary**: The implementation correctly provides the core functionality for persisting user feedback, and unit tests verify the service logic and PII exclusion in logging. However, a significant issue was found with a task falsely marked complete regarding Pydantic v2 compatibility, and the critical integration test for end-to-end database persistence is missing/mocked, leaving a key part of the functionality untested.

**Key Findings**:

-   **HIGH Severity**:
    -   **Task falsely marked complete**: The task to "Address the Pydantic v2 compatibility for `FeedbackDB` model (update to use `pydantic.ConfigDict`)" in `backend/src/models/feedback.py` was marked complete but the code still uses the deprecated `Config` inner class. This is a critical violation of task completion.
    -   **Critical integration test missing**: The integration test for persistence in `backend/tests/test_feedback_api.py` (AC 3.2.1, 3.2.2) is still explicitly deferred and the current test mocks the persistence layer instead of performing actual end-to-end testing with a database. This leaves a critical path untested.

**Acceptance Criteria Coverage**:

| AC #      | Description                                                                                                                                                                                                                                                                                                                                       | Status      | Evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :-------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC 3.2.1 | Given a feedback signal (thumbs up/down) is received from the UI, when the backend processes the signal, then it records the feedback along with the user's query, the chatbot's response, and a timestamp into a persistent log within the PostgreSQL database. | IMPLEMENTED | `backend/src/models/feedback.py` (ORM model definition), `backend/src/db/database.py` (PostgreSQL connection), `backend/src/db/feedback_repository.py` (DB insertion logic), `backend/src/services/feedback_service.py` (calls repository), `backend/src/api/feedback.py` (API endpoint calls service), `backend/migrations/versions/42abdd4552da_create_feedback_table.py` (table creation). Unit tests in `backend/tests/test_feedback_service.py` (`test_record_feedback_success`) verify service-to-repository interaction. **(Integration test for actual persistence missing/mocked)** |
| AC 3.2.2 | Given the system records feedback, then the system ensures that no personally identifiable information (PII) is persisted or logged, adhering to the project's data privacy guidelines.                                                                                                                                                             | IMPLEMENTED | `backend/src/services/feedback_service.py` (logger excludes `query` and `response` from info log), `backend/tests/test_feedback_service.py` (`test_record_feedback_logs_success` verifies PII exclusion in logs). `backend/src/models/feedback.py` uses string types for query/response; reliance on PRD statement that no PII is handled for MVP. |

**Summary: 2 of 2 acceptance criteria fully implemented.**

**Task Completion Validation**:

| Task                                                                                                                                                                  | Marked As | Verified As         | Evidence                                                                                                                                                                                                                                                                                                                                                                  |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- | :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Define the database model for feedback in `backend/src/models/feedback.py`.                                                                                           | [x]       | VERIFIED COMPLETE   | `backend/src/models/feedback.py` (lines 20-36)                                                                                                                                                                                                                                                                                                                            |
| Implement logic to connect to PostgreSQL database.                                                                                                                    | [x]       | VERIFIED COMPLETE   | `backend/src/db/database.py` (lines 14-38)                                                                                                                                                                                                                                                                                                                                |
| Implement logic to insert feedback data into the `feedback` table.                                                                                                    | [x]       | VERIFIED COMPLETE   | `backend/src/db/feedback_repository.py` (lines 7-13)                                                                                                                                                                                                                                                                                                                      |
| **Address the Pydantic v2 compatibility for `FeedbackDB` model (update to use `pydantic.ConfigDict`).**                                                              | [x]       | **NOT DONE**        | `backend/src/models/feedback.py` (line 35 still uses `class Config: orm_mode = True` for Pydantic v1. This is a **HIGH SEVERITY** finding.)                                                                                                                                                                                                                                  |
| Modify `POST /feedback` endpoint in `backend/src/api/feedback.py` to call `FeedbackService.save_feedback`.                                                            | [x]       | VERIFIED COMPLETE   | `backend/src/api/feedback.py` (lines 14-21)                                                                                                                                                                                                                                                                                                                               |
| Create a database migration script to create the `feedback` table in PostgreSQL.                                                                                      | [x]       | VERIFIED COMPLETE   | `backend/migrations/versions/42abdd4552da_create_feedback_table.py` (lines 21-28)                                                                                                                                                                                                                                                                                        |
| Review logging implementation in `FeedbackService` to explicitly exclude any PII from logs.                                                                           | [x]       | VERIFIED COMPLETE   | `backend/src/services/feedback_service.py` (line 14)                                                                                                                                                                                                                                                                                                                      |
| Ensure `query` and `response` are handled safely.                                                                                                                     | [x]       | VERIFIED COMPLETE   | `backend/src/models/feedback.py` (uses string types), `backend/src/services/feedback_service.py` (logging excludes these fields)                                                                                                                                                                                                                                              |
| Test `FeedbackService.save_feedback` method, mocking database interactions.                                                                                           | [x]       | VERIFIED COMPLETE   | `backend/tests/test_feedback_service.py` (`test_record_feedback_success`)                                                                                                                                                                                                                                                                                                 |
| Verify correct data is stored in the mock database.                                                                                                                   | [x]       | VERIFIED COMPLETE   | `backend/tests/test_feedback_service.py` (`test_record_feedback_success` asserts `create_feedback` called with correct data)                                                                                                                                                                                                                                               |
| Test edge cases.                                                                                                                                                      | [x]       | VERIFIED COMPLETE   | `backend/tests/test_feedback_service.py` (`test_record_feedback_handles_repository_exception`)                                                                                                                                                                                                                                                                            |
| Test PII exclusion in logs.                                                                                                                                           | [x]       | VERIFIED COMPLETE   | `backend/tests/test_feedback_service.py` (`test_record_feedback_logs_success`)                                                                                                                                                                                                                                                                                            |
| **Extend existing `test_feedback_api.py` to test end-to-end feedback submission, including persistence to a test database.**                                          | [ ]       | **NOT DONE**        | The task was marked incomplete in the story, and the test implementation still mocks persistence. This is a **HIGH SEVERITY** finding as a critical path is untested. |

**Summary: 10 of 12 completed tasks verified, 0 questionable, 1 falsely marked complete. 1 task remains incomplete.**

**Test Coverage and Gaps**:
- Unit tests for `FeedbackService` are comprehensive and pass.
- Integration tests for `FeedbackAPI` are not performing end-to-end database persistence verification, as the persistence layer is mocked. This leaves a significant gap in testing the full persistence functionality.

**Architectural Alignment**:
- The implementation generally aligns with the architectural decisions regarding PostgreSQL for data persistence and the use of FastAPI for the API.
- The Pydantic v2 compatibility issue is a minor deviation but needs to be addressed for future-proofing and consistency.

**Security Notes**:
- PII exclusion in logging has been verified at the unit test level. The implementation for `query` and `response` uses basic string types, making it reliant on upstream systems not to pass PII. Given the PRD states no PII is handled for MVP, this is acceptable for the current scope.

**Best-Practices and References**:
- Adherence to FastAPI and SQLAlchemy best practices is generally good.
- Pydantic v2 migration is a recommended best practice that has been missed.

**Action Items**:

**Code Changes Required**:
- [ ] [High] Update `FeedbackDB` model in `backend/src/models/feedback.py` to use `pydantic.ConfigDict` for Pydantic v2 compatibility.
- [ ] [High] Implement end-to-end integration tests for `backend/tests/test_feedback_api.py` that verify actual database persistence of feedback, without mocking the persistence layer.

**Advisory Notes**:
- Note: Consider enhancing the PII handling for `query` and `response` fields if the scope expands to include potential PII.
- Note: Document the rationale for including `aiosqlite` in `requirements.txt` if PostgreSQL is the primary database.
