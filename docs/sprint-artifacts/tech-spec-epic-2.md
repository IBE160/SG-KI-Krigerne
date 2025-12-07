# Epic Technical Specification: Core Question Answering

Date: Wednesday, December 3, 2025
Author: BIP
Epic ID: 2
Status: Draft

---

## Overview

This Technical Specification outlines the implementation details for Epic 2: Core Question Answering, as defined in the Product Requirements Document (PRD) for the Himolde Study Friend project. This epic is central to the MVP's value proposition, focusing on enabling students to retrieve accurate and instant answers to course-related questions using natural language. It builds upon the foundational chat interface and knowledge base established in Epic 1, integrating the Retrieval-Augmented Generation (RAG) architecture to deliver conversational responses and handle scenarios where information is not found.

## Objectives and Scope

**In-Scope:**
- **Natural Language Query Input (FR1):** Users can ask questions about course information using natural language, with the backend capable of identifying intent and key entities (e.g., course codes).
- **Knowledge Base Retrieval (FR6, FR7, FR8):** The system will search a structured knowledge base (defined in Epic 1) to retrieve specific information (learning outcomes, exam formats, mandatory assignments) based on the identified intent and entities.
- **Conversational Response Generation (FR3):** Retrieved information will be formatted into clear, conversational responses and delivered in real-time to the user via the chat interface.
- **"I Don't Know" Scenarios (FR10):** The chatbot will politely inform the user when it cannot find a relevant answer in the knowledge base, preventing misleading information.

**Out-of-Scope (for this Epic):**
- UI/UX elements outside the core chat interaction (e.g., user profiles, advanced settings).
- Integration with external university systems (e.g., Canvas, student information systems).
- Complex multi-turn conversations beyond direct Q&A.
- User authentication.

## System Architecture Alignment

This epic directly aligns with the AI Application, Backend API, and Real-time Communication decisions detailed in the project's Architecture Document. The RAG architecture, leveraging the Gemini API for LLM integration and PostgreSQL with pgvector for the vector database, is central to this epic's functionality. The backend will expose REST endpoints for query input and utilize Server-Sent Events (SSE) or streaming HTTP for efficient one-way streaming of partial answers to the frontend, ensuring real-time responsiveness as per the architectural design. Data persistence relies on the PostgreSQL database, established in Epic 1, to store and retrieve course information effectively.

## Detailed Design

### Services and Modules

- **Chat Service (Backend):**
    - **Responsibilities:** Orchestrates the core Q&A flow. Receives user queries, identifies intent/entities, invokes knowledge base retrieval, and generates conversational responses.
    - **Inputs:** User natural language query (string), session context (if multi-turn becomes relevant later).
    - **Outputs:** Streaming text responses (via SSE), formatted according to `ux_design_content` principles.
    - **Owner:** Backend Team

- **Knowledge Base Retrieval Module (Backend):**
    - **Responsibilities:** Searches the structured knowledge base (PostgreSQL + pgvector) for relevant course information based on identified intent and entities.
    - **Inputs:** Parsed intent (e.g., `get_exam_format`), entities (e.g., `course_code: TDT4140`).
    - **Outputs:** Retrieved information (e.g., `exam_format` string), or a "not found" signal.
    - **Owner:** Backend Team

- **Response Generation Module (Backend):**
    - **Responsibilities:** Formats retrieved information into natural language conversational responses. Handles "I don't know" scenarios.
    - **Inputs:** Retrieved information (string), "not found" signal.
    - **Outputs:** Formatted conversational response (string).
    - **Owner:** Backend Team

### Data Models and Contracts

- **Course Information (as stored in PostgreSQL):**
    - `course_code`: PRIMARY KEY, VARCHAR(20) - e.g., "MAT110"
    - `name`: VARCHAR(255) - e.g., "Introduction to Mathematics"
    - `description`: TEXT
    - `learning_outcomes`: TEXT - Markdown formatted list
    - `exam_format`: VARCHAR(255) - e.g., "4-hour written exam"
    - `mandatory_assignments`: TEXT - Markdown formatted list
    - `embedding`: VECTOR(1536) - For `pgvector` semantic search

- **User Query (Frontend -> Backend):**
    - `query_text`: string - User's natural language question.

- **Chat Response (Backend -> Frontend - Streaming via SSE):**
    - `{ "type": "chunk", "content": "..." }`
    - `{ "type": "done" }`

### APIs and Interfaces

- **POST /chat (Streaming HTTP/SSE):**
    - **Purpose:** Primary endpoint for user interaction, sending natural language queries and receiving streaming conversational responses.
    - **Request:** `application/json`
        ```json
        {
          "query_text": "What are the learning outcomes for MAT110?"
        }
        ```
    - **Response:** `text/event-stream` (SSE)
        ```
        data: {"type": "chunk", "content": "The learning outcomes for MAT110 "}
        data: {"type": "chunk", "content": "include understanding basic calculus"}
        data: {"type": "done"}
        ```
    - **Error Codes:** Non-2xx HTTP status with JSON `{ "error": "message", "code": "SOME_CODE" }`.

### Workflows and Sequencing

1.  **User Input:**
    *   User types a question into the frontend chat interface (FR1).
    *   Frontend sends `query_text` via `POST /chat` to the backend.
2.  **Backend Processing:**
    *   **Intent/Entity Recognition:** Backend Chat Service receives the `query_text`, processes it to identify user intent (e.g., `get_learning_outcomes`) and relevant entities (e.g., `course_code: MAT110`).
    *   **Knowledge Base Retrieval (FR6, FR7, FR8):** The Retrieval Module queries the PostgreSQL database (potentially using `pgvector` for semantic search on the `embedding` field) to find information matching the identified intent and entities.
    *   **Response Generation (FR3, FR10):**
        *   If relevant information is retrieved: The Generation Module formats the data into a conversational natural language response.
        *   If no relevant information is found (from KB Retrieval): The Generation Module crafts a polite "I don't know" message.
    *   **Streaming Response:** The backend streams the generated response back to the frontend chunk by chunk via SSE.
3.  **Frontend Display:**
    *   Frontend receives streaming chunks and displays them in the chat history area in real-time (FR4).
    *   User sees the full conversational response.

## Non-Functional Requirements

### Performance

- **Response Time:** Chatbot responses for known queries (after initial RAG processing) should be delivered to the user within 1-2 seconds. This aligns with the PRD's goal of a fluid conversational experience and the Architecture's decision to use streaming HTTP (SSE).
- **System Responsiveness:** The web interface and backend API must remain highly responsive during user interaction, even under moderate load, as specified in the PRD and UX Design. This will be supported by efficient database queries (indexed PostgreSQL) and optimized API calls to Gemini.

### Security

- **Data Privacy:** User interactions will be anonymized; no Personally Identifiable Information (PII) will be collected or stored. This aligns with the PRD's scope and the Architecture's decision for no user authentication in MVP.
- **Knowledge Base Integrity:** Access to the PostgreSQL database will be restricted to a dedicated DB user with minimum necessary permissions. Database credentials and Gemini API keys will be stored as environment variables on the deployment platform (Railway), not hardcoded. HTTPS will be enforced for all traffic.
- **AI Safety:** Prompt instructions will be used to guide the Gemini model and mitigate risks of prompt injection. Full prompts and answers will not be logged to prevent accidental exposure of sensitive information, as outlined in the Architecture.

### Reliability/Availability

- **Availability:** The system (frontend and backend) should aim for high availability. Vercel and Railway's managed services contribute to this, with redundancy and automated scaling where possible.
- **Recovery:** In case of backend service failure, the frontend should gracefully display an error message (as per UX Design error patterns) and allow the user to retry the query. Data persistence in PostgreSQL ensures that course information is not lost.

### Observability

- **Logging:** Python's built-in `logging` module will be used in the backend to record key events (e.g., chat requests, database errors, Gemini API failures) at DEBUG, INFO, WARNING, and ERROR levels. Logs will be output to the console for collection by the hosting platform (Railway).
- **Metrics/Tracing:** While not a primary MVP focus, the architecture should allow for easy integration of monitoring metrics and distributed tracing in future iterations. The use of FastAPI and its ecosystem supports this.

## Dependencies and Integrations

- **Frontend Dependencies (himolde-study-friend/package.json):**
    - **Vite:** `^5.0.0` (Build tool, dev server)
    - **React:** `^18.2.0` (UI library)
    - **TypeScript:** `^5.2.2` (Language)
    - **Tailwind CSS:** `^3.3.0` (Utility-first CSS framework)
    - **shadcn/ui:** `~0.8.0` (UI component library, built on Radix UI and Tailwind)
    - **PostCSS, Autoprefixer:** (Tailwind CSS tooling)
    - **Vitest:** (Testing framework - planned)
    - **ESLint, Prettier:** (Linting and formatting - planned)

- **Backend Dependencies (backend/requirements.txt):**
    - **Python:** `3.11.14` or `3.12.2` (Runtime)
    - **FastAPI:** `^0.122.0` (Web framework)
    - **Pydantic:** (Data validation)
    - **SQLAlchemy / Psycopg2:** (PostgreSQL ORM/driver - planned)
    - **psycopg2-binary:** (PostgreSQL adapter)
    - **pgvector:** `~0.5.0` (PostgreSQL extension for vector embeddings)
    - **python-dotenv:** (Environment variable management)
    - **Pytest:** (Testing framework - planned)
    - **Black, Flake8:** (Linting and formatting - planned)

- **AI Service:**
    - **Gemini API:** (LLM for conversational responses)

- **Database:**
    - **PostgreSQL:** `^16.0` (Relational database with `pgvector` extension)

- **Integration Points:**
    - **Frontend to Backend:** REST API calls (`/chat` for streaming, other endpoints for data) via HTTP/SSE.
    - **Backend to Database:** Python ORM/library (e.g., SQLAlchemy) for data access.
    - **Backend to Gemini API:** Direct HTTP requests.
    - **CI/CD:** GitHub Actions for automated testing and deployment.

## Acceptance Criteria (Authoritative)

The following acceptance criteria are derived directly from the user stories within Epic 2: Core Question Answering, as defined in `epics.md`. Each criterion is atomic, testable, and contributes to the successful delivery of the epic's core functionality.

### Story 2.1: Implement Natural Language Query Input
1.  **Given** the user has entered a question (e.g., "what is the exam format for TDT4140?"),
2.  **When** they send the message,
3.  **Then** the system backend receives the raw text of the question.
4.  **And** the backend identifies the user's core intent (e.g., `get_exam_format`) and the key entity (e.g., `course_code: TDT4140`).

### Story 2.2: Implement Knowledge Base Retrieval
1.  **Given** a parsed intent (e.g., `get_exam_format`) and entity (e.g., `course_code: TDT4140`),
2.  **When** the retrieval component is invoked,
3.  **Then** it searches the `knowledge_base.json` (or PostgreSQL equivalent) for the matching course.
4.  **And** it extracts the specific information requested (e.g., the value of the `exam_format` field for `TDT4140`).
5.  **And** if no matching course or information is found, it returns a "not found" signal.

### Story 2.3: Generate Conversational Responses
1.  **Given** the system has retrieved a piece of information (e.g., "4-hour written exam"),
2.  **When** the generation component is invoked,
3.  **Then** it formats this information into a natural language sentence (e.g., "The exam format for TDT4140 is a 4-hour written exam.").
4.  **And** the generated response is sent back to the UI within 2 seconds.
5.  **And** the response appears in the chat history for the user.

### Story 2.4: Handle "I Don't Know" Scenarios
1.  **Given** the retrieval component returned a "not found" signal,
2.  **When** the generation component is invoked,
3.  **Then** it creates a polite and clear "I don't know" response (e.g., "I'm sorry, I couldn't find the information for that course. You may want to check the official course page.").
4.  **And** the "I don't know" response is displayed to the user in the chat window.

## Traceability Mapping

| AC Source (Story.AC#) | Spec Section(s)            | Component(s)/API(s)                  | Test Idea                                       |
| :-------------------- | :------------------------- | :----------------------------------- | :---------------------------------------------- |
| 2.1.3                 | Workflows and Sequencing   | Chat Service (Backend), POST /chat   | Verify backend receives raw query text.         |
| 2.1.4                 | Workflows and Sequencing   | Chat Service (Backend)               | Verify intent and entity extraction for sample queries. |
| 2.2.3                 | Workflows and Sequencing   | Knowledge Base Retrieval Module      | Test retrieval for existing courses/info.       |
| 2.2.4                 | Workflows and Sequencing   | Knowledge Base Retrieval Module      | Test extraction of specific info for a course.  |
| 2.2.5                 | Workflows and Sequencing   | Knowledge Base Retrieval Module      | Test "not found" signal for non-existent data.  |
| 2.3.3                 | Workflows and Sequencing   | Response Generation Module           | Verify natural language formatting of retrieved data. |
| 2.3.4                 | Performance                | Response Generation Module, POST /chat | Measure response time for generated answers.    |
| 2.3.5                 | Workflows and Sequencing   | Frontend Display                     | Verify response appears in chat history.        |
| 2.4.3                 | Workflows and Sequencing   | Response Generation Module           | Test "I don't know" message for failed retrievals. |
| 2.4.4                 | Workflows and Sequencing   | Frontend Display                     | Verify "I don't know" message appears in chat window.

## Risks, Assumptions, Open Questions

### Risks

-   **R1: LLM Hallucinations/Inaccuracy:** There is an inherent risk that the Gemini API may generate inaccurate or fabricated information, despite the RAG architecture.
    -   **Mitigation:** Strict adherence to grounding responses in the knowledge base, careful prompt engineering, and the "I Don't Know" scenario handling (FR10) to avoid providing misleading information. User feedback mechanism (Epic 3) will help identify and rectify instances.
-   **R2: Knowledge Base Coverage:** The initial knowledge base might not contain all information users seek, leading to frequent "I Don't Know" responses.
    -   **Mitigation:** Clear communication of scope (MVP focuses on specific course info), and continuous expansion of the knowledge base post-MVP. User feedback can highlight gaps.
-   **R3: Performance Degradation:** High concurrency or complex queries could lead to response times exceeding the 1-2 second target.
    -   **Mitigation:** Database indexing, efficient API calls, and streaming responses as per architecture. Performance testing will identify and address bottlenecks.

### Assumptions

-   **A1: Knowledge Base Content:** The structured knowledge base (initially JSON, later PostgreSQL) will be accurately maintained and updated with course information.
-   **A2: Gemini API Availability & Cost:** The Gemini API will remain accessible and its usage costs will be within acceptable project budget limits.
-   **A3: User Acceptance:** Students will adopt and find value in a conversational interface for course information.

### Open Questions

-   **Q1: Multi-turn Conversation:** To what extent will the system need to support multi-turn conversations (e.g., "What about MAT110?" after asking about TDT4140)? (Currently out of scope for MVP).
-   **Q2: Source Citation:** Should the chatbot provide citations or links to the source documents within its responses for increased trust? (Future enhancement consideration).

## Test Strategy Summary

The test strategy for Epic 2 will focus on validating the core question-answering functionality, ensuring accuracy, responsiveness, and appropriate handling of known and unknown queries.

-   **Unit Testing (Backend):**
    -   **Framework:** Pytest.
    -   **Coverage:** Individual components of the Chat Service, Knowledge Base Retrieval Module, and Response Generation Module. This includes testing intent/entity recognition, database queries, response formatting, and "I Don't Know" logic.
-   **Integration Testing (Backend):**
    -   **Framework:** Pytest with FastAPI's TestClient.
    -   **Coverage:** End-to-end flow from receiving a `POST /chat` request to generating a streaming response. Verify correct integration between Chat Service, Knowledge Base Retrieval, Response Generation, and Gemini API interaction (mocked if necessary).
-   **UI Testing (Frontend):**
    -   **Framework:** Vitest with React Testing Library.
    -   **Coverage:** Verification that user input is correctly sent, streaming responses are displayed in real-time, and "I Don't Know" messages are rendered as expected.
-   **Acceptance Criteria Testing (End-to-End):**
    -   **Methodology:** Manual and automated tests based directly on the Acceptance Criteria listed above. This will involve a fixed set of test questions covering known courses and information types, as well as questions designed to trigger "I Don't Know" scenarios.
    -   **Focus:** Confirming the 80% accuracy target (PRD Success Criteria) for known queries.
-   **Performance Testing:**
    -   **Methodology:** Load testing on the `POST /chat` endpoint to ensure response times remain within the 1-2 second target under simulated user load.
-   **Security Testing:**
    -   **Methodology:** Basic checks for prompt injection vulnerabilities and ensuring no sensitive data is logged.
