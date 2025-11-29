# ibe160 - Epic Breakdown

**Author:** BIP
**Date:** 2025-11-29
**Project Level:** {{project_level}}
**Target Scale:** {{target_scale}}

---

## Overview

This document provides the complete epic and story breakdown for ibe160, decomposing the requirements from the [PRD](./PRD.md) into implementable stories.

**Living Document Notice:** This is the initial version. It will be updated after UX Design and Architecture workflows add interaction and technical details to stories.

## Epics Summary

The project is broken down into three core epics, designed to deliver incremental value. We start with a foundational epic to establish the application, followed by the core question-answering functionality, and finally, a feedback loop for continuous improvement. This approach ensures that a visible, functional product is established early, with the most critical user value delivered in the second stage.

*   **Epic 1: Foundation & Core Chat Interface**
    *   **Value:** Establishes the essential technical foundation, a structured knowledge base, and a working, responsive chat UI. This delivers the visible application and the backend structure needed for all future functionality.
    *   **Sequencing:** This must be the first epic as it sets up the entire project infrastructure.

*   **Epic 2: Core Question Answering**
    *   **Value:** Enables students to get instant, accurate answers to their most common course-related questions. This delivers the core value proposition of the MVP.
    *   **Sequencing:** Depends on the Foundation epic to provide the UI and knowledge base structure.

*   **Epic 3: User Feedback Loop**
    *   **Value:** Allows users to help improve the system's accuracy over time, making the chatbot more reliable and trustworthy.
    *   **Sequencing:** Depends on the Question Answering epic, as feedback can only be given on an existing answer.

---

## Functional Requirements Inventory

## Functional Requirements Inventory

This inventory lists all functional requirements (FRs) extracted from the PRD. It will be used to ensure complete coverage in the epic and story breakdown.

- **FR1:** The user can ask questions about course information in natural language.
- **FR2:** The system shall provide a conversational interface for user interaction.
- **FR3:** The system shall provide responses in a clear and conversational manner.
- **FR4:** The user shall receive real-time message delivery from the chatbot.
- **FR5:** The user can provide feedback on the helpfulness of the chatbot's answers.
- **FR6:** The system can retrieve learning outcomes for a specific course.
- **FR7:** The system can retrieve the exam format for a specific course.
- **FR8:** The system can retrieve information about mandatory assignments for a specific course.
- **FR9:** The system shall provide answers derived from a structured knowledge base.
- **FR10:** The system shall indicate when it cannot find an answer to a user's question.
- **FR11:** The system's knowledge base can be updated with new or changed course information.
- **FR12:** The knowledge base shall be structured to support accurate information retrieval.
- **FR13:** The user can interact with the chatbot through a web-based interface.
- **FR14:** The web interface shall be responsive and work on both desktop and mobile browsers.

---

## FR Coverage Map

## FR Coverage Map

This map shows which Functional Requirements (FRs) are addressed by each epic.

### Epic 1: Foundation & Core Chat Interface
*This epic covers the setup of the user-facing application and the backend data structures.*
- **FR2:** The system shall provide a conversational interface for user interaction.
- **FR4:** The user shall receive real-time message delivery from the chatbot.
- **FR9:** The system shall provide answers derived from a structured knowledge base.
- **FR11:** The system's knowledge base can be updated with new or changed course information.
- **FR12:** The knowledge base shall be structured to support accurate information retrieval.
- **FR13:** The user can interact with the chatbot through a web-based interface.
- **FR14:** The web interface shall be responsive and work on both desktop and mobile browsers.

### Epic 2: Core Question Answering
*This epic delivers the primary functionality of understanding questions and providing answers.*
- **FR1:** The user can ask questions about course information in natural language.
- **FR3:** The system shall provide responses in a clear and conversational manner.
- **FR6:** The system can retrieve learning outcomes for a specific course.
- **FR7:** The system can retrieve the exam format for a specific course.
- **FR8:** The system can retrieve information about mandatory assignments for a specific course.
- **FR10:** The system shall indicate when it cannot find an answer to a user's question.

### Epic 3: User Feedback Loop
*This epic focuses on creating a mechanism for continuous improvement.*
- **FR5:** The user can provide feedback on the helpfulness of the chatbot's answers.

---

## Epic 1: Foundation & Core Chat Interface

**Goal:** Establish the essential technical foundation, a structured knowledge base, and a working, responsive chat UI. This delivers the visible application and the backend structure needed for all future functionality.

### Story 1.1: Project Initialization & CI/CD Pipeline Setup

As a **Developer**,
I want **a standardized project structure and an automated CI/CD pipeline**,
So that **I can ensure consistent development practices and reliable deployments**.

**Acceptance Criteria:**

- **Given** a new project is needed,
- **When** the initialization script is run,
- **Then** a standard folder structure (e.g., `src`, `docs`, `tests`) is created.
- **And** a `package.json` (or equivalent) with core dependencies (e.g., a web framework, test runner) is created.
- **And** a basic "Hello World" version of the app can be run locally.
- **And** a CI/CD pipeline (e.g., GitHub Actions) is configured to automatically run linters and basic tests on every push.

**Prerequisites:** None

**Technical Notes:** Use Vite for the React frontend and Vitest for testing. Set up basic linting with ESLint. The CI/CD pipeline should use GitHub Actions.

### Story 1.2: Design and Implement the Knowledge Base Schema

As a **System**,
I want **a well-defined and structured knowledge base schema**,
So that **course information can be stored accurately and retrieved efficiently**.

**Acceptance Criteria:**

- **Given** course data needs to be stored,
- **When** the knowledge base is created,
- **Then** a JSON file (`knowledge_base.json`) is created with a clear schema.
- **And** the schema supports fields for `course_code`, `learning_outcomes`, `exam_format`, and `mandatory_assignments`.
- **And** the system can programmatically load and parse this JSON file without errors.
- **And** an initial dummy course is added to the file for testing purposes.

**Prerequisites:** Story 1.1

**Technical Notes:** This fulfills FR12 (structured KB) and supports FR9 (answers from KB). The manual update process for the MVP (FR11) will involve editing this JSON file directly.

### Story 1.3: Build the Basic Chat Interface UI

As a **User**,
I want **a simple and clean web interface**,
So that **I can easily interact with the chatbot**.

**Acceptance Criteria:**

- **Given** the user opens the web app,
- **When** the page loads,
- **Then** a chat window is displayed.
- **And** the chat window contains a message history area (initially with a welcome message) and a text input field with a "Send" button.
- **And** the interface is responsive, rendering correctly on both desktop (e.g., 1920px width) and mobile (e.g., 375px width) screen sizes.

**Prerequisites:** Story 1.1

**Technical Notes:** Implements FR13 (web interface), FR14 (responsive), and the visual shell for FR2 (conversational interface). Use basic HTML/CSS and a lightweight React component library.

### Story 1.4: Implement Real-Time Message Handling in the UI

As a **User**,
I want **my messages to appear instantly in the chat window and receive a response**,
So that **the conversation feels fluid and real-time**.

**Acceptance Criteria:**

- **Given** the user has typed a message,
- **When** they click "Send" or press Enter,
- **Then** their message immediately appears in the message history area.
- **And** the input field is cleared.
- **And** the system will immediately respond with a hardcoded "echo" of the user's message.
- **And** the "echo" response also appears in the message history.

**Prerequisites:** Story 1.3

**Technical Notes:** This covers FR4 (real-time message delivery). This simulates the real-time feel before the actual AI backend is connected. Implement using React state management for message list and input handling.

---

## EPIC 1 REVIEW - Complete Breakdown

**Epic 1: Foundation & Core Chat Interface**
**Goal:** Establish the essential technical foundation, a structured knowledge base, and a working, responsive chat UI.

**Stories (4 total):**

- **Story 1.1: Project Initialization & CI/CD Pipeline Setup**
  - User Story: As a Developer, I want a standardized project structure and an automated CI/CD pipeline, so that I can ensure consistent development practices and reliable deployments.
  - Acceptance Criteria: Project structure created, `package.json` with dependencies, basic "Hello World" runs, CI/CD for linting/tests.
  - Prerequisites: None

- **Story 1.2: Design and Implement the Knowledge Base Schema**
  - User Story: As a System, I want a well-defined and structured knowledge base schema, so that course information can be stored accurately and retrieved efficiently.
  - Acceptance Criteria: `knowledge_base.json` created with schema for course info, system can parse, initial dummy course.
  - Prerequisites: Story 1.1

- **Story 1.3: Build the Basic Chat Interface UI**
  - User Story: As a User, I want a simple and clean web interface, so that I can easily interact with the chatbot.
  - Acceptance Criteria: Chat window with history and input, responsive on desktop/mobile.
  - Prerequisites: Story 1.1

- **Story 1.4: Implement Real-Time Message Handling in the UI**
  - User Story: As a User, I want my messages to appear instantly in the chat window and receive a response, so that the conversation feels fluid and real-time.
  - Acceptance Criteria: User message appears immediately, input cleared, system echoes message, echo appears in history.
  - Prerequisites: Story 1.3

**Review Questions to Consider:**

- **Is the story sequence logical?** Yes, the stories build progressively from project setup to a basic interactive UI.
- **Are acceptance criteria clear and testable?** Yes, they provide concrete conditions for validation.
- **Are there any missing stories for the FRs this epic covers?** No, all assigned FRs (FR2, FR4, FR9, FR11, FR12, FR13, FR14) are addressed.
- **Are the stories sized appropriately (single dev agent session)?** Yes, each story is focused and self-contained, suitable for rapid iteration.
- **FRs covered by this epic:** FR2, FR4, FR9, FR11, FR12, FR13, FR14.

<!-- Repeat for each epic (N = 1, 2, 3...) -->

## Epic 2: Core Question Answering

**Goal:** Enable students to get instant, accurate answers to their most common course-related questions. This delivers the core value proposition of the MVP.

### Story 2.1: Implement Natural Language Query Input

As a **User**,
I want **to ask questions about course information in natural language**,
So that **I can find information without needing to know specific commands or keywords**.

**Acceptance Criteria:**

- **Given** the user has entered a question (e.g., "what is the exam format for TDT4140?"),
- **When** they send the message,
- **Then** the system backend receives the raw text of the question.
- **And** the backend identifies the user's core intent (e.g., `get_exam_format`) and the key entity (e.g., `course_code: TDT4140`).

**Prerequisites:** Story 1.4

**Technical Notes:** This is the entry point for the RAG pipeline. The initial implementation can use simple keyword matching or regex to determine intent and entities. This covers FR1.

### Story 2.2: Implement Knowledge Base Retrieval

As a **System**,
I want **to retrieve relevant information from the knowledge base based on the user's query**,
So that **I can provide accurate, grounded answers**.

**Acceptance Criteria:**

- **Given** a parsed intent (e.g., `get_exam_format`) and entity (e.g., `course_code: TDT4140`),
- **When** the retrieval component is invoked,
- **Then** it searches the `knowledge_base.json` for the matching course.
- **And** it extracts the specific information requested (e.g., the value of the `exam_format` field for `TDT4140`).
- **And** if no matching course or information is found, it returns a "not found" signal.

**Prerequisites:** Story 1.2, Story 2.1

**Technical Notes:** This component is the "Retriever" in the RAG architecture. It directly addresses FR6, FR7, and FR8 by being able to get the data.

### Story 2.3: Generate Conversational Responses

As a **User**,
I want **to receive answers in a clear and conversational format**,
So that **the information is easy to understand**.

**Acceptance Criteria:**

- **Given** the system has retrieved a piece of information (e.g., "4-hour written exam"),
- **When** the generation component is invoked,
- **Then** it formats this information into a natural language sentence (e.g., "The exam format for TDT4140 is a 4-hour written exam.").
- **And** the generated response is sent back to the UI.
- **And** the response appears in the chat history for the user.

**Prerequisites:** Story 2.2

**Technical Notes:** This is the "Generator" in the RAG architecture. It fulfills FR3. For the MVP, this can be a set of simple response templates.

### Story 2.4: Handle "I Don't Know" Scenarios

As a **User**,
I want **the chatbot to tell me when it doesn't know the answer**,
So that **I am not misled and know I need to look elsewhere**.

**Acceptance Criteria:**

- **Given** the retrieval component returned a "not found" signal,
- **When** the generation component is invoked,
- **Then** it creates a polite and clear "I don't know" response (e.g., "I'm sorry, I couldn't find the information for that course. You may want to check the official course page.").
- **And** the "I don't know" response is displayed to the user in the chat window.

**Prerequisites:** Story 2.2

**Technical Notes:** This directly implements FR10 and is a critical part of building user trust.

---

## EPIC 2 REVIEW - Complete Breakdown

**Epic 2: Core Question Answering**
**Goal:** Enable students to get instant, accurate answers to their most common course-related questions.

**Stories (4 total):**

- **Story 2.1: Implement Natural Language Query Input**
  - User Story: As a User, I want to ask questions about course information in natural language, so that I can find information without needing to know specific commands or keywords.
  - Acceptance Criteria: Backend receives question, identifies intent and entity.
  - Prerequisites: Story 1.4

- **Story 2.2: Implement Knowledge Base Retrieval**
  - User Story: As a System, I want to retrieve relevant information from the knowledge base based on the user's query, so that I can provide accurate, grounded answers.
  - Acceptance Criteria: Searches KB for course/info, extracts specific data, returns "not found" if applicable.
  - Prerequisites: Story 1.2, Story 2.1

- **Story 2.3: Generate Conversational Responses**
  - User Story: As a User, I want to receive answers in a clear and conversational format, so that the information is easy to understand.
  - Acceptance Criteria: Formats retrieved info into natural language sentence, sends to UI, appears in chat history.
  - Prerequisites: Story 2.2

- **Story 2.4: Handle "I Don't Know" Scenarios**
  - User Story: As a User, I want the chatbot to tell me when it doesn't know the answer, so that I am not misled and know I need to look elsewhere.
  - Acceptance Criteria: Creates polite "I don't know" response and displays it when retrieval fails.
  - Prerequisites: Story 2.2

**Review Questions to Consider:**

- **Is the story sequence logical?** Yes, the stories progressively build the core Q&A functionality.
- **Are acceptance criteria clear and testable?** Yes, they provide concrete conditions for validation.
- **Are there any missing stories for the FRs this epic covers?** No, all assigned FRs (FR1, FR3, FR6, FR7, FR8, FR10) are addressed.
- **Are the stories sized appropriately (single dev agent session)?** Yes, each story is focused and self-contained.
- **FRs covered by this epic:** FR1, FR3, FR6, FR7, FR8, FR10.

<!-- Repeat for each epic (N = 1, 2, 3...) -->

## Epic 3: User Feedback Loop

**Goal:** Allow users to help improve the system's accuracy over time, making the chatbot more reliable and trustworthy.

### Story 3.1: Implement User Feedback Mechanism in UI

As a **User**,
I want **to easily provide feedback on the chatbot's answers**,
So that **the system can be improved**.

**Acceptance Criteria:**

- **Given** a chatbot response is displayed,
- **When** the response is rendered,
- **Then** "thumbs up" (👍) and "thumbs down" (👎) icons are displayed next to the response.
- **And** clicking either icon sends a feedback signal to the backend.
- **And** after providing feedback, the icons change state (e.g., become greyed out or show a "Thank you" message) to indicate feedback was received.

**Prerequisites:** Story 1.3, Story 2.3

**Technical Notes:** This implements the UI part of FR5.

### Story 3.2: Persist User Feedback

As a **System**,
I want **to store user feedback**,
So that **it can be analyzed to improve the chatbot's performance**.

**Acceptance Criteria:**

- **Given** a feedback signal (thumbs up/down) is received from the UI,
- **When** the backend processes the signal,
- **Then** it records the feedback along with the user's query, the chatbot's response, and a timestamp into a persistent log (e.g., a simple JSON file or database entry).
- **And** the system logs do not contain any personally identifiable information (PII) from the user.

**Prerequisites:** Story 3.1

**Technical Notes:** This implements the backend persistence for FR5.

---

## EPIC 3 REVIEW - Complete Breakdown

**Epic 3: User Feedback Loop**
**Goal:** Allow users to help improve the system's accuracy over time, making the chatbot more reliable and trustworthy.

**Stories (2 total):**

- **Story 3.1: Implement User Feedback Mechanism in UI**
  - User Story: As a User, I want to easily provide feedback on the chatbot's answers, so that the system can be improved.
  - Acceptance Criteria: Thumbs up/down icons displayed, clicking sends signal to backend, icons change state.
  - Prerequisites: Story 1.3, Story 2.3

- **Story 3.2: Persist User Feedback**
  - User Story: As a System, I want to store user feedback, so that it can be analyzed to improve the chatbot's performance.
  - Acceptance Criteria: Backend records feedback with query, response, and timestamp in a log, no PII.
  - Prerequisites: Story 3.1

**Review Questions to Consider:**

- **Is the story sequence logical?** Yes, the stories build the feedback loop from UI to backend.
- **Are acceptance criteria clear and testable?** Yes, they provide concrete conditions for validation.
- **Are there any missing stories for the FRs this epic covers?** No, the two stories fully address FR5.
- **Are the stories sized appropriately (single dev agent session)?** Yes, each story is a focused and manageable task.
- **FRs covered by this epic:** FR5.

<!-- End epic repeat -->

---

## FR Coverage Matrix

This matrix confirms that all functional requirements (FRs) from the PRD have been mapped to a specific epic and story.

| FR # | Requirement Description | Epic | Story |
| :--- | :--- | :--- | :--- |
| FR1 | User can ask questions in natural language. | 2 | 2.1 |
| FR2 | System shall provide a conversational interface. | 1 | 1.3 |
| FR3 | System shall provide responses in a clear and conversational manner. | 2 | 2.3 |
| FR4 | User shall receive real-time message delivery. | 1 | 1.4 |
| FR5 | User can provide feedback on the helpfulness of the chatbot's answers. | 3 | 3.1, 3.2 |
| FR6 | System can retrieve learning outcomes for a specific course. | 2 | 2.2 |
| FR7 | System can retrieve the exam format for a specific course. | 2 | 2.2 |
| FR8 | System can retrieve information about mandatory assignments. | 2 | 2.2 |
| FR9 | System shall provide answers derived from a structured knowledge base. | 1 | 1.2 |
| FR10| System shall indicate when it cannot find an answer. | 2 | 2.4 |
| FR11| System's knowledge base can be updated. | 1 | 1.2 |
| FR12| Knowledge base shall be structured to support accurate information retrieval. | 1 | 1.2 |
| FR13| User can interact with the chatbot through a web-based interface. | 1 | 1.3 |
| FR14| Web interface shall be responsive. | 1 | 1.3 |

---

## Summary

## Summary

**✅ Epic Breakdown Complete**

**Created:** `epics.md` with epic and story breakdown

**FR Coverage:** All 14 functional requirements from the PRD have been successfully mapped to stories across the three epics, ensuring full traceability and coverage.

**Context Incorporated:**
- ✅ PRD requirements
- ✅ Product Brief vision and goals

**Status:** COMPLETE - The initial epic and story breakdown is ready.

**Next Steps:**
- The `epics.md` document is now complete with the initial breakdown.
- This document can be used to inform further UX Design or Architecture workflows (if not already done).
- It is now ready for Phase 4: Implementation (Sprint Planning and detailed task assignment to development teams).

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._

_This document will be updated after UX Design and Architecture workflows to incorporate interaction details and technical decisions._
