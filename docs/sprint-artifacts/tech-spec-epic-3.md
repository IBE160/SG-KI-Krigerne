# Epic Technical Specification: User Feedback Loop

Date: Thursday, December 4, 2025
Author: BIP
Epic ID: 3
Status: Draft

---

## Overview

The Himolde Study Friend project aims to centralize course information through an AI-powered chatbot, enhancing the student experience by providing instant and accurate answers to student queries. Epic 3, specifically the "User Feedback Loop", focuses on allowing users to help improve the system's accuracy over time, making the chatbot more reliable and trustworthy. This epic is crucial for continuous improvement and building user trust in the chatbot's responses.

## Objectives and Scope

This section outlines the specific objectives and scope of Epic 3: User Feedback Loop.

**In-scope:**
*   **FR5:** The user can provide feedback on the helpfulness of the chatbot's answers.
*   **Story 3.1: Implement User Feedback Mechanism in UI:**
    *   Display "thumbs up" (👍) and "thumbs down" (👎) icons next to chatbot responses.
    *   Send feedback signal to the backend upon icon click.
    *   Change icon state to indicate feedback received.
*   **Story 3.2: Persist User Feedback:**
    *   Backend records feedback with user's query, chatbot's response, and timestamp.
    *   Ensure logged feedback does not contain Personally Identifiable Information (PII).

**Out-of-scope (based on overall MVP and current epic focus):**
*   Direct integration with complex university systems (e.g., student information systems, Canvas APIs).
*   User authentication, personalized profiles, or custom dashboards.
*   Support for multiple languages.
*   Advanced conversational features beyond basic Q&A.
*   Analysis or reporting of feedback data (this is for future iterations).
*   Implementing AI model retraining based on feedback (future iteration).

## System Architecture Alignment

Epic 3: User Feedback Loop aligns directly with the established system architecture by leveraging both the frontend and backend components. The frontend (Vite + React SPA) will implement the user interface for feedback mechanisms (e.g., thumbs up/down icons), consistent with the `shadcn/ui` and Tailwind CSS styling decisions. The backend (Python REST API with FastAPI) will provide endpoints to receive and process this feedback. Data persistence for feedback will utilize PostgreSQL, aligning with the chosen database for structured data storage. This epic builds upon the core chat interface and question-answering capabilities established in previous epics, integrating seamlessly into the existing component structure and communication patterns (REST API calls).

## Detailed Design

### Services and Modules

**Frontend Module:**
*   **`FeedbackDisplay` Component (`frontend/src/components/FeedbackDisplay.tsx`):**
    *   **Responsibility:** Renders the thumbs up/down icons adjacent to each chatbot message. Handles user interaction (click events) on these icons.
    *   **Input:** Chatbot message content, user query.
    *   **Output:** Dispatches feedback signal to the `ApiClient`.

**Backend Modules:**
*   **`FeedbackAPI` Endpoint (`backend/src/api/feedback.py`):**
    *   **Responsibility:** Defines the REST endpoint for receiving user feedback. Validates incoming request data.
    *   **Input:** HTTP POST request with feedback payload.
    *   **Output:** HTTP 200 OK on success, HTTP 400/500 on error.
*   **`FeedbackService` (`backend/src/services/feedback_service.py`):**
    *   **Responsibility:** Encapsulates the business logic for processing and persisting user feedback. Interacts with the `Database` layer.
    *   **Input:** Validated feedback data.
    *   **Output:** Confirmation of persistence or error.
*   **`FeedbackRepository` (`backend/src/db/feedback_repository.py`):**
    *   **Responsibility:** Handles direct database operations related to the `Feedback` entity (e.g., insert, query).
    *   **Input:** `Feedback` entity/model.
    *   **Output:** Database transaction result.

### Data Models and Contracts

**PostgreSQL Database Model (`Feedback` table):**
```sql
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    rating INTEGER NOT NULL, -- 1 for thumbs up, -1 for thumbs down
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    session_id UUID -- Optional, for future session context (not PII)
);
```

**Backend Pydantic Model (`backend/src/models/feedback.py`):**
```python
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class FeedbackBase(BaseModel):
    query: str = Field(..., description="The user's original query.")
    response: str = Field(..., description="The chatbot's response that was rated.")
    rating: int = Field(..., description="User rating: 1 for thumbs up, -1 for thumbs down.", ge=-1, le=1)

class FeedbackCreate(FeedbackBase):
    # This model is used for incoming feedback data from the API
    pass

class FeedbackDB(FeedbackBase):
    id: UUID
    timestamp: datetime
    session_id: UUID | None = None

    class Config:
        from_attributes = True # Formerly orm_mode = True
```

**Frontend TypeScript Interface (`frontend/src/types/feedback.ts`):**
```typescript
interface FeedbackData {
  query: string;
  response: string;
  rating: 1 | -1; // 1 for thumbs up, -1 for thumbs down
  sessionId?: string; // Optional session ID
}
```

### APIs and Interfaces

**Backend API Endpoint:**
*   **Method:** `POST`
*   **Path:** `/feedback`
*   **Description:** Allows users to submit feedback on chatbot responses.
*   **Request Body:** `application/json` (conforms to `FeedbackCreate` Pydantic model)
    ```json
    {
      "query": "What is the exam format for MAT100?",
      "response": "The exam format for MAT100 is a 4-hour written exam.",
      "rating": 1
    }
    ```
*   **Responses:**
    *   `200 OK`: `application/json`
        ```json
        {
          "data": {
            "message": "Feedback received successfully."
          }
        }
        ```
    *   `422 Unprocessable Entity`: If request body fails validation (FastAPI default).
    *   `500 Internal Server Error`: For unhandled server-side exceptions.

**Frontend API Client Interface (`frontend/src/lib/api-client.ts`):**
```typescript
interface ApiClient {
  // ... other API methods
  sendFeedback(feedbackData: FeedbackData): Promise<{ message: string }>;
}
```

### Workflows and Sequencing

**Workflow: User Feedback Submission**

1.  **User Receives Chatbot Response:** A chatbot message (`response`) is displayed in the UI, following a user's `query`.
2.  **UI Renders Feedback Controls:** The `FeedbackDisplay` component (Story 3.1) renders "thumbs up" (👍) and "thumbs down" (👎) icons alongside the chatbot response.
3.  **User Provides Feedback:** The user clicks on either the 👍 or 👎 icon, indicating their satisfaction with the response.
4.  **Frontend Captures Data:** The `FeedbackDisplay` component captures the `query`, `response`, and the `rating` (1 for 👍, -1 for 👎).
5.  **Frontend Sends Feedback:** The `ApiClient` (`frontend/src/lib/api-client.ts`) invokes its `sendFeedback` method, making a `POST` request to the `/feedback` endpoint on the backend, passing the captured data.
6.  **Backend Receives Request:** The `FeedbackAPI` endpoint (`backend/src/api/feedback.py`) receives the `POST /feedback` request.
7.  **Backend Validates Data:** The incoming JSON payload is validated against the `FeedbackCreate` Pydantic model.
8.  **Backend Processes Feedback:** The `FeedbackAPI` endpoint calls `FeedbackService` (`backend/src/services/feedback_service.py`) to handle the business logic of storing the feedback.
9.  **Backend Persists Feedback:** The `FeedbackService` calls `FeedbackRepository` (`backend/src/db/feedback_repository.py`) to interact with the PostgreSQL database, inserting a new record into the `feedback` table.
10. **Backend Responds:** The backend sends a `200 OK` response to the frontend, indicating successful feedback submission.
11. **Frontend Updates UI:** The `FeedbackDisplay` component updates its state (e.g., greys out icons, displays a "Thank you" message) to provide visual confirmation to the user that their feedback has been recorded.

## Non-Functional Requirements

### Performance

*   **Frontend Responsiveness:** User feedback submission (clicking 👍/👎) should be non-blocking and feel instantaneous from the user's perspective. The UI should update visually to acknowledge feedback within 100ms.
*   **Backend Response Time:** The `POST /feedback` endpoint should process requests and persist data to the database within 500ms, even under moderate load, to ensure it does not contribute to perceived system lag.
*   **Database Write Latency:** Database writes for feedback records should complete quickly to minimize resource consumption and ensure timely data capture.

### Security

*   **Data Privacy (PII):** The feedback data collected (query, response, rating, timestamp, optional session ID) explicitly excludes Personally Identifiable Information (PII) to comply with data privacy regulations.
*   **Endpoint Protection:** The `POST /feedback` API endpoint will implement basic rate-limiting to mitigate risks of abuse, spamming, or denial-of-service attacks, aligning with the overall security architecture.
*   **Database Access:** The database user configured for the backend service will have minimum necessary permissions, limited to `INSERT` operations on the `feedback` table, adhering to the principle of least privilege.

### Reliability/Availability

*   **Feedback Mechanism Availability:** The feedback submission feature should be highly available. A temporary failure in feedback recording (e.g., database connection issue) should not disrupt the user's primary chat experience. The chatbot should continue to function even if feedback cannot be persisted.
*   **Graceful Degradation:** In case of backend errors during feedback persistence, the frontend should gracefully handle the error (e.g., log it internally, inform the user with a subtle `Toast` if appropriate, but allow continued interaction with the chatbot).
*   **Data Integrity:** Mechanisms (e.g., database constraints) will ensure that recorded feedback data is consistent and valid.

### Observability

*   **Logging:** The backend will implement logging for feedback submission events.
    *   Successful feedback submissions will be logged at an `INFO` level, including details like the rating, timestamp, and potentially a truncated version of the query/response (without PII).
    *   Failed feedback persistence attempts (e.g., database errors) will be logged at an `ERROR` level, with relevant exception details.
*   **Traceability:** Each feedback submission should be associated with a unique request ID (if applicable in the overall system) to facilitate tracing requests through the system.

## Dependencies and Integrations

**Frontend Dependencies:**
*   **React:** `^18.2.0` (Core UI library)
*   **shadcn/ui:** `~0.8.0` (UI component library built on Radix UI and Tailwind CSS)
*   **Tailwind CSS:** `^3.3.0` (Utility-first CSS framework for styling)
*   **Custom API Client:** `frontend/src/lib/api-client.ts` (Handles HTTP communication with the backend).

**Backend Dependencies:**
*   **FastAPI:** `^0.122.0` (Web framework for building the API endpoint)
*   **Pydantic:** (For data validation of incoming feedback requests, version as per overall backend `requirements.txt`)
*   **SQLAlchemy/asyncpg (or similar):** (Python library for interacting with PostgreSQL, version as per overall backend `requirements.txt`)
*   **psycopg2 (or similar):** (PostgreSQL adapter for Python, version as per overall backend `requirements.txt`)

**Integrations:**
*   **PostgreSQL Database:** The backend service integrates with the PostgreSQL database for durable storage of user feedback.
*   **Frontend-Backend HTTP Communication:** Standard REST API calls (POST requests to `/feedback`) facilitate the communication between the frontend `FeedbackDisplay` component and the backend `FeedbackAPI` endpoint.

## Acceptance Criteria (Authoritative)

The following acceptance criteria are derived from Epic 3's stories and define the testable conditions for successful implementation:

1.  **AC 3.1.1:** Given a chatbot response is displayed, when the response is rendered, then "thumbs up" (👍) and "thumbs down" (👎) icons are displayed next to the response.
2.  **AC 3.1.2:** Given "thumbs up" or "thumbs down" icons are displayed, when a user clicks either icon, then a feedback signal is sent to the backend.
3.  **AC 3.1.3:** Given feedback has been sent, when the icons are displayed, then they change state (e.g., become greyed out or show a "Thank you" message) to indicate feedback was received.
4.  **AC 3.2.1:** Given a feedback signal is received by the backend, when the backend processes the signal, then it records the feedback along with the user's query, the chatbot's response, and a timestamp into the persistent `feedback` table.
5.  **AC 3.2.2:** Given feedback is recorded, then the persisted feedback record contains the user's `query`, the chatbot's `response`, the `rating` (1 or -1), and a `timestamp`.
6.  **AC 3.2.3:** Given feedback is recorded, then the persisted feedback record does not contain any personally identifiable information (PII) from the user.

## Traceability Mapping

| AC      | Spec Section(s)                                                                       | Component(s)/API(s)                                    | Test Idea                                                                                                     |
| :------ | :------------------------------------------------------------------------------------ | :----------------------------------------------------- | :------------------------------------------------------------------------------------------------------------ |
| 3.1.1   | UX Design: 7.1 Consistency (Feedback Patterns); Detailed Design: Services and Modules | `FeedbackDisplay` (Frontend)                           | Verify 👍/👎 icons are rendered alongside bot messages in various states (initial, after feedback).          |
| 3.1.2   | UX Design: 7.1 Consistency (Feedback Patterns); Detailed Design: APIs and Interfaces  | `FeedbackDisplay` (Frontend), `POST /feedback` (Backend) | Simulate user click on icons and assert `POST /feedback` call is made with correct payload.                 |
| 3.1.3   | UX Design: 7.1 Consistency (Feedback Patterns)                                        | `FeedbackDisplay` (Frontend)                           | Verify UI state change (e.g., icons grey out, "Thank you" message) after successful feedback submission.     |
| 3.2.1   | Detailed Design: Data Models, Workflows and Sequencing                                | `POST /feedback` (Backend), `FeedbackService`, `FeedbackRepository` | Send feedback, query database directly to confirm new record insertion.                                       |
| 3.2.2   | Detailed Design: Data Models, Workflows and Sequencing                                | `FeedbackService` (Backend)                            | Verify `query`, `response`, `rating`, `timestamp` fields are correctly populated in the database record.    |
| 3.2.3   | Detailed Design: Data Models; NFR: Security                                           | `FeedbackService` (Backend)                            | Test with sample data to ensure no PII is inadvertently stored; inspect database for PII leakage.            |

## Risks, Assumptions, Open Questions

**Risks:**
*   **User Misinterpretation of Feedback Mechanism:** Users might misunderstand the purpose of the 👍/👎 icons or provide inconsistent/inaccurate feedback, potentially leading to misleading data for future improvements.
*   **Feedback Endpoint Abuse/Spam:** Without robust rate-limiting and input validation, the `POST /feedback` endpoint could be targeted by automated scripts, leading to an influx of irrelevant or malicious data, impacting database performance and data quality.
*   **Performance Degradation (Database):** A high volume of feedback submissions, especially if not adequately indexed or if the database connection pool is saturated, could degrade the overall performance of the backend service.

**Assumptions:**
*   **Genuine User Intent:** It is assumed that users providing feedback intend to genuinely assist in improving the chatbot's responses.
*   **No PII in Core Data:** The `query` and `response` fields, as designed to be stored, are assumed not to contain any Personally Identifiable Information (PII) as the chatbot's domain is strictly course information. This assumption is critical for compliance.
*   **Future Feedback Analysis:** This epic primarily focuses on the *collection* and *persistence* of feedback. The analysis, categorization, and utilization of this feedback for model improvement are assumed to be part of future epics.
*   **"Thumbs Up/Down" Sufficient:** For the MVP, a simple binary "good/bad" feedback mechanism is assumed to be sufficient to gather initial insights.

**Open Questions:**
*   **Feedback Data Retention Policy:** What is the long-term data retention policy for collected feedback? How long should it be stored?
*   **"Session_ID" Generation and Usage:** If a `session_id` is introduced in the future for richer context, how will it be generated, transmitted, and ensured to remain non-PII?
*   **User Ability to Modify/Delete Feedback:** Will users have the ability to review, modify, or delete their previously submitted feedback? (Currently out of MVP scope).

## Test Strategy Summary

The test strategy for Epic 3 will encompass unit, integration, and acceptance testing, focusing on the correct functioning and non-functional aspects of the feedback loop.

*   **Unit Tests:**
    *   **Frontend (`FeedbackDisplay`):** Jest/Vitest will be used to test the rendering of the 👍/👎 icons, their click handlers, and the component's state changes (e.g., showing "Thank you" after feedback). Mocking the `ApiClient` will isolate component behavior.
    *   **Backend (`FeedbackAPI`, `FeedbackService`, `FeedbackRepository`):** Pytest will be used to test the Fast API endpoint's request validation, the `FeedbackService`'s business logic, and the `FeedbackRepository`'s interaction with a test database (e.g., using a test fixture or in-memory SQLite for repository isolation).
*   **Integration Tests:**
    *   **Frontend-Backend API:** End-to-end tests will verify the complete flow from user clicking a feedback icon in the UI to the backend successfully receiving and acknowledging the `POST /feedback` request. This will involve using tools like Playwright or Cypress (if integrated into the frontend project) or direct API calls from frontend test suite.
    *   **Backend-Database:** Tests will confirm that the `FeedbackService` correctly interacts with an actual (test) PostgreSQL instance, ensuring data is persisted and retrieved as expected.
*   **Acceptance Criteria (AC) Testing:** Each Acceptance Criteria (AC) outlined in Section 7 will have corresponding manual and/or automated test cases to ensure full functional coverage.
*   **Non-Functional Testing:**
    *   **Performance:** Basic load testing using tools like Locust or `ab` (ApacheBench) on the `POST /feedback` endpoint to ensure the 500ms response time is met under anticipated load.
    *   **Security:** Manual and automated checks (e.g., OWASP ZAP) will verify rate-limiting effectiveness and ensure no PII is stored in the database.
    *   **Accessibility:** Manual keyboard navigation tests and automated checks (e.g., axe DevTools) for the `FeedbackDisplay` component to ensure WCAG 2.1 Level AA compliance.
