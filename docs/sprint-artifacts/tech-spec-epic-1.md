# Epic Technical Specification: Foundation & Core Chat Interface

Date: Tuesday, December 2, 2025
Author: BIP
Epic ID: 1
Status: Draft

---

## Overview

The Himolde Study Friend project aims to address the significant frustration and inefficiency students face when searching for basic course information. By developing an AI-powered chatbot, the project seeks to centralize course data and provide instant, accurate answers to student queries.

This technical specification details the implementation for **Epic 1: Foundation & Core Chat Interface**. The primary goal of this epic is to establish the essential technical foundation for the entire application. This includes setting up the project structure, creating an initial version of the knowledge base schema, and building a working, responsive chat user interface to deliver a visible, functional product early and provide the backend structure needed for all future functionality.

## Objectives and Scope

**In-Scope:**
*   **Project Initialization:** A standardized Vite + React (TypeScript) frontend and Python backend project structure will be created.
*   **CI/CD Pipeline:** A basic CI/CD pipeline using GitHub Actions will be configured to run linters and tests on every push.
*   **Knowledge Base Schema:** A well-defined JSON schema for the knowledge base (`knowledge_base.json`) will be designed and implemented to store course information accurately.
*   **Basic Chat UI:** A simple, responsive web interface will be built, including a message history area and a text input field, adhering to WCAG 2.1 Level AA.
*   **Real-Time Message Simulation:** The UI will implement a simulated real-time message flow where user messages are immediately displayed and "echoed" back by the system.

**Out-of-Scope:**
*   **AI/LLM Integration:** This epic does not include any integration with the Gemini API or the implementation of the RAG architecture.
*   **Natural Language Processing:** The system will not perform any natural language understanding; it will only echo user input.
*   **User Feedback Mechanism:** The UI will not include any user feedback features like "thumbs up/down".
*   **User Authentication:** No user login or personalization features will be implemented.

## System Architecture Alignment

The work in this epic directly implements the foundational layers of the system as defined in the `architecture.md` document.

*   **Project Structure:** The creation of the `frontend/` and `backend/` directories with their internal source structures (`src/`, `components/`, `api/`, `services/`, etc.) realizes the prescribed project layout.
*   **Technology Stack:** The initialization of the Vite + React frontend and the Python backend using the specified `npm` and `pip` commands aligns with the chosen **Vite + React (TS)** and **Python/FastAPI** stack.
*   **Database:** The design and creation of the `knowledge_base.json` file serves as the initial, file-based implementation of the data persistence layer, which the architecture specifies will later evolve into a PostgreSQL database.
*   **Frontend UI:** Building the basic chat UI with `shadcn/ui` and Tailwind CSS directly follows the decisions made in the **Styling** and **UI Components** sections of the architecture.
*   **CI/CD:** Setting up GitHub Actions for linting and testing establishes the initial **Quality** and **Deployment** infrastructure.

## Detailed Design

### Services and Modules

#### Frontend (`frontend/`)
| Module/Component | Responsibility | Inputs | Outputs |
|---|---|---|---|
| `App.tsx` | Main application component, routes to pages. | - | Rendered `ChatPage`. |
| `pages/ChatPage.tsx` | Renders the main chat interface. | - | Full chat UI. |
| `components/ChatWindow.tsx` | Displays the history of chat messages. | Array of messages. | Rendered list of `ChatMessage` components. |
| `components/ChatMessage.tsx` | Renders a single user or bot message bubble. | Message object (text, sender). | Styled message bubble. |
| `components/ChatInput.tsx` | Handles user text input and the "Send" button. | User typing event. | "Send" button click event with message text. |
| `lib/api-client.ts` | Manages communication with the backend API. | Message text to send. | Response from the backend. |

#### Backend (`backend/`)
| Module/Service | Responsibility | Inputs | Outputs |
|---|---|---|---|
| `main.py` | FastAPI application entry point. | HTTP requests. | HTTP responses. |
| `api/chat.py` | Defines the `/chat/echo` API endpoint. | User message in request body. | JSON response with the echoed message. |
| `services/EchoService.py` | Contains the business logic for the echo service. | A string message. | The same string message. |

### Data Models and Contracts

The initial data model for this epic is a simple, file-based JSON structure.

#### `knowledge_base.json`

This file will be the single source of truth for all course information in the MVP. It will contain an array of course objects.

**Schema:**

```json
[
  {
    "course_code": "string",
    "learning_outcomes": "string",
    "exam_format": "string",
    "mandatory_assignments": "string"
  }
]
```

**Example:**
```json
[
  {
    "course_code": "TDT4140",
    "learning_outcomes": "The student has deep knowledge of software design principles and patterns...",
    "exam_format": "4-hour written digital exam",
    "mandatory_assignments": "3 out of 4 assignments must be approved."
  }
]
```

### APIs and Interfaces

For this foundational epic, a single, simple REST endpoint will be created to simulate the chat functionality.

#### `POST /api/chat/echo`

*   **Description:** Receives a message from the user and returns the same message.
*   **Request Body:**
    ```json
    {
      "message": "Hello, world!"
    }
    ```
*   **Success Response (200 OK):**
    ```json
    {
      "reply": "Hello, world!"
    }
    ```
*   **Error Response (400 Bad Request):** If the message is empty or missing.
    ```json
    {
      "error": "Message cannot be empty."
    }
    ```

### Workflows and Sequencing

The user interaction flow for this epic is a simple request-response loop that simulates a real chat conversation.

1.  **User Input:** The user types a message into the `ChatInput` component and clicks "Send".
2.  **UI Update (User):** The `ChatPage` immediately adds the user's message to its state and re-renders the `ChatWindow`, displaying the new user message. The input field is cleared.
3.  **API Call:** The `api-client` sends a `POST` request to the `/api/chat/echo` endpoint with the user's message.
4.  **Backend Processing:** The `EchoService` in the backend receives the message and immediately returns it in a JSON response.
5.  **API Response:** The `api-client` receives the JSON response from the backend.
6.  **UI Update (Bot):** The `ChatPage` adds the "reply" from the response to its state as a bot message, which triggers a re-render of the `ChatWindow` to display the bot's echoed message.

## Non-Functional Requirements

### Performance

*   **API Response Time:** The `/api/chat/echo` endpoint must respond in **< 200ms** to ensure the user experience feels instantaneous and fluid.
*   **UI Responsiveness:** The frontend interface must remain highly responsive, with UI updates for sending and receiving messages happening without any noticeable lag.

### Security

*   **Knowledge Base Integrity:** The `knowledge_base.json` file on the server should have file permissions set to prevent unauthorized modification by any process other than the designated admin or update script.
*   **Dependency Management:** All backend dependencies listed in `requirements.txt` should be regularly scanned for known vulnerabilities.
*   **No Sensitive Information:** No personally identifiable information (PII) or other sensitive data will be handled or stored in this epic.

### Reliability/Availability

*   **Availability:** The web application should be consistently available to users.
*   **Error Handling:** The backend service should handle invalid requests (e.g., empty messages) gracefully with a `400 Bad Request` response and not crash. The frontend should not crash if it receives an error from the backend.

### Observability

*   **Logging:** The Python backend will use the built-in `logging` module.
    *   `INFO` level logs will be generated for each incoming request to the `/api/chat/echo` endpoint.
    -   `ERROR` level logs will be generated for any unhandled exceptions or server errors.
*   **Log Output:** Logs will be written to the console to be collected by the hosting platform (e.g., Railway).

## Dependencies and Integrations

#### Frontend (`package.json`)
*   **Vite:** Build tool and development server.
*   **React:** Core UI library.
*   **TypeScript:** Language for type safety.
*   **Tailwind CSS:** Utility-first CSS framework for styling.
*   **shadcn/ui:** UI component library.
*   **Vitest:** Testing framework.
*   **ESLint:** Linter for code quality.

#### Backend (`requirements.txt`)
*   **FastAPI:** High-performance web framework for building the API.
*   **Uvicorn:** ASGI server to run the FastAPI application.
*   **Pydantic:** Data validation and settings management.
*   **Pytest:** Framework for backend testing.
*   **Black / Flake8:** Code formatting and linting.

#### Integrations
*   **GitHub Actions:** For Continuous Integration and Continuous Deployment (CI/CD).

## Acceptance Criteria (Authoritative)

1.  **Given** the project is initialized, **Then** a standard frontend and backend folder structure exists.
2.  **Given** the project is initialized, **Then** a `package.json` and `requirements.txt` are created with the core dependencies.
3.  **Given** the project is initialized, **Then** a basic "Hello World" version of the frontend and backend can be run locally.
4.  **Given** a push to the repository, **Then** a CI/CD pipeline automatically runs linters and basic tests for both frontend and backend.
5.  **Given** the knowledge base is created, **Then** a `knowledge_base.json` file exists with a valid schema supporting `course_code`, `learning_outcomes`, `exam_format`, and `mandatory_assignments`.
6.  **Given** the app is running, **Then** the system can programmatically load and parse the `knowledge_base.json` file without errors.
7.  **Given** a user opens the web app, **Then** a chat window is displayed containing a message history area and a text input field with a "Send" button.
8.  **Given** a user opens the web app, **Then** the interface is responsive and renders correctly on both desktop (1920px) and mobile (375px) screen sizes.
9.  **Given** a user interacts with the UI, **Then** all interactive elements meet WCAG 2.1 Level AA accessibility standards.
10. **Given** a user sends a message, **Then** their message immediately appears in the message history, and the input field is cleared.
11. **Given** a user sends a message, **Then** the system backend responds by echoing the user's message.
12. **Given** the backend has responded, **Then** the echoed response appears in the message history.

## Traceability Mapping

| AC # | Spec Section(s) | Component(s) / API(s) | Test Idea |
|---|---|---|---|
| 1-3 | Dependencies | Project Initialization Scripts | Run init scripts and verify folder structure and "Hello World" app runs. |
| 4 | Dependencies | `.github/workflows/` | Create a PR to trigger the CI/CD pipeline and verify that linters and tests run. |
| 5-6 | Data Models | `backend/services/KnowledgeBaseService.py` | Write a unit test to load and parse a sample `knowledge_base.json`. |
| 7 | Detailed Design | `frontend/pages/ChatPage.tsx` | End-to-end test with a tool like Playwright to check for UI elements. |
| 8 | (Implicit) | `frontend/styles/` | Visual regression testing or manual check on different screen sizes. |
| 9 | (Implicit) | All `frontend/components/` | Run accessibility audit tools (e.g., axe) on the rendered components. |
| 10 | Workflows | `frontend/components/ChatInput.tsx` | Unit test the component's state change on send. E2E test the full flow. |
| 11 | APIs and Interfaces | `backend/api/chat.py` (`/api/chat/echo`) | Integration test sending a POST request and asserting the response. |
| 12 | Workflows | `frontend/components/ChatWindow.tsx` | E2E test to verify the echoed message appears in the chat history. |

## Risks, Assumptions, Open Questions

*   **Risk:** The chosen UI library (`shadcn/ui`) might have a steeper learning curve than anticipated for some developers, potentially impacting initial development velocity.
    *   **Mitigation:** Allocate dedicated time for initial component exploration and provide clear examples or a small component playground.
*   **Assumption:** The file-based `knowledge_base.json` will be sufficient for the MVP's performance and scalability needs for the initially small dataset of course information.
*   **Question:** What is the long-term strategy for managing updates to the `knowledge_base.json` file in a production environment (e.g., manual process, dedicated CMS, integration with university systems)? This needs to be defined for future epics.

## Test Strategy Summary

The testing strategy for this epic will cover multiple levels to ensure code quality, functionality, and user experience.

*   **Unit Tests:**
    *   **Frontend:** `Vitest` will be used to test individual React components (e.g., `ChatMessage`, `ChatInput`) in isolation, verifying their rendering and state management logic.
    *   **Backend:** `Pytest` will be used to test individual functions and methods within the backend services (e.g., `EchoService`) and API endpoints, ensuring correct logic and data handling.
*   **Integration Tests:**
    *   Tests will be written to verify the communication between the frontend's `api-client` and the backend's `/api/chat/echo` endpoint, ensuring that requests are sent and responses are handled correctly.
*   **End-to-End (E2E) Tests:**
    *   `Playwright` will be utilized to simulate a full user journey, from typing a message in the UI, sending it, to verifying that the echoed response appears correctly in the chat history. These tests will run against the deployed application or a local development environment.
*   **Accessibility Tests:**
    *   Automated accessibility checks using tools like `axe DevTools` or `Lighthouse` will be integrated into the CI/CD pipeline.
    *   Manual keyboard navigation and screen reader testing will be performed on key UI components to ensure WCAG 2.1 Level AA compliance.

## Post-Review Follow-ups

*   **Story 1.3**:
    *   Implement robust automated tests for desktop responsiveness (AC5) [file: himolde-study-friend/src/components/ChatWindow.test.tsx]
    *   Implement robust automated tests for mobile responsiveness (AC6) [file: himolde-study-friend/src/components/ChatWindow.test.tsx]
    *   Implement robust automated tests for keyboard navigation accessibility (AC7) [file: himolde-study-friend/src/components/ChatWindow.test.tsx]
    *   Implement robust automated tests for color contrast accessibility (AC8) [file: himolde-study-friend/src/components/ChatWindow.test.tsx]
    *   Implement robust automated tests for `aria-labels` accessibility (AC9) [file: himolde-study-friend/src/components/ChatWindow.test.tsx]

