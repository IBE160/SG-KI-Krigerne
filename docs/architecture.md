# Architecture

## Executive Summary

The Himolde Study Friend project aims to centralize course information through an AI-powered chatbot, providing instant and accurate answers to student queries, thereby enhancing the student experience. This initiative focuses solely on course data, ensuring no personal data is handled. The architecture will be kept simple with one backend service and a single knowledge base for Retrieval-Augmented Generation (RAG), supported by a manual or simple import pipeline. Streaming responses will be used to provide immediate user feedback.

The core functionality revolves around an AI-powered chatbot providing instant, accurate answers to student queries about course information. Non-functional requirements emphasize quick response times (1-2 seconds), high system responsiveness, WCAG 2.1 Level AA accessibility, and security for knowledge base integrity. The UX design leverages `shadcn/ui` with a "Structured Clarity" direction, focusing on a minimalist chat interface, responsive design across devices, and subtle visual feedback mechanisms like typing indicators and message states. Real-time message delivery is a core UI requirement.

## Project Initialization

Project initialization will involve the following sequence of commands to set up the Vite + React (TypeScript) frontend, integrated with Tailwind CSS and shadcn/ui:

```bash
# 1. Create Vite project with React and TypeScript
npm create vite@latest himolde-study-friend -- --template react-ts

# 2. Navigate into project directory
cd himolde-study-friend

# 3. Install project dependencies
npm install

# 4. Install Tailwind CSS and its peer dependencies
npm install -D tailwindcss postcss autoprefixer

# 5. Initialize Tailwind CSS and PostCSS configuration
npx tailwindcss init -p

# 6. Install @types/node for path resolution
npm install -D @types/node

# 7. Initialize shadcn/ui (interactive prompt)
npx shadcn-ui@latest init
```

**Starter-Provided Architectural Decisions (from Vite + React-TS template):**

-   **Language/TypeScript:** Provided. The project will use TypeScript for type safety and improved developer experience.
-   **Styling Solution:** While Vite provides basic CSS handling, we will explicitly integrate **Tailwind CSS** as our utility-first CSS framework and `shadcn/ui` for high-quality, accessible UI components.
-   **Testing Framework:** Not directly provided by the Vite template; a testing framework (e.g., Vitest) will need to be integrated separately.
-   **Linting/Formatting:** Not directly provided; tools like ESLint and Prettier will be integrated separately for code quality and consistency.
-   **Build Tooling:** Provided by **Vite** for a fast development server and **Rollup** for optimized production builds.
-   **Project Structure:** Provided by Vite, including a logical layout for source code (`src/`), public assets (`public/`), and configuration files (`vite.config.ts`, `package.json`).

Project initialization using the above commands should be the first implementation story.

## Decision Summary

| Category | Decision | Status | Affects Epics | Rationale |
| -------- | -------- | ------ | ------------- | --------- |
| Frontend | Framework | Chosen | All           | Vite + React (TS) for SPA with fast dev server. |
| Frontend | Language | Chosen | All           | TypeScript for type safety. |
| Frontend | Styling  | Chosen | All           | Tailwind CSS + shadcn/ui for UI components. |
| Build    | Tooling  | Chosen | All           | Vite/Rollup for fast development and optimized builds. |
| Project  | Structure| Chosen | All           | Vite default project structure. |
| Backend  | API Pattern | Chosen | All Client-facing | REST is simple, well-understood, and sufficient for MVP; aligns with 'one backend service' and clarity goals. |
| Data     | Persistence | Chosen | Core Q&A, KB Mgmt | PostgreSQL is ideal for structured, relational course data and provides a solid foundation for future vector search capabilities. |
| AI       | Application | Chosen | Core Q&A      | Gemini API for LLM integration, PostgreSQL with pgvector for the vector database, and a lightweight custom RAG orchestration flow in the backend for simplicity and direct Gemini API interaction. |
| Real-time| Communication| Chosen | User Interaction | Server-Sent Events (SSE) or streaming HTTP for efficient one-way streaming of partial answers, avoiding unnecessary WebSocket complexity for the MVP. |
| Deployment| Target    | Chosen | All           | Vercel for frontend (Vite React SPA) for ease of deployment and performance; Railway for backend service and PostgreSQL for developer-friendly managed hosting, balancing simplicity and best practices. |
| Quality  | Testing Framework | Chosen | All           | Vitest for fast, modern frontend testing; Pytest for comprehensive Python backend testing. |
| Quality  | Linting/Formatting| Chosen | All           | ESLint + Prettier for frontend (TypeScript, React) and Black + Flake8 for backend (Python) to ensure code quality and consistency. |
| Cross-cutting| Date/time handling | Chosen | All           | Store all times in DB as UTC ISO-8601. Frontend converts to user's local time and friendly format. Python backend uses timezone-aware datetime in UTC. Simple, robust, and sufficient for MVP. |
| Cross-cutting| Authentication| Chosen | All           | No user authentication for MVP; access is anonymous. Backend protected with rate limiting and basic abuse protection. Aligns with frictionless access and no personal data for MVP. Future versions may add university SSO. |
| Cross-cutting| Error Handling | Chosen | All           | Frontend: Error Boundary for critical crashes, inline error messages/toast for network/backend issues. Backend: Consistent HTTP status codes and JSON error objects ({error: 'message', code: 'SOME_CODE'}). |
| Cross-cutting| Logging Strategy | Chosen | All           | Python's built-in `logging` module with DEBUG, INFO, WARNING, ERROR levels. Logs to console for hosting platform collection. Focus on key events (chat requests, DB/RAG errors, LLM failures), avoiding secrets/API keys. |
| Cross-cutting| API response format | Chosen | All Client-facing | `/chat` streaming endpoint: SSE/HTTP with JSON chunks ({ "type": "chunk", "content": "..." }) and final ({ "type": "done" }). Other REST endpoints: `200 OK` with `{"data": ...}` JSON object. Predictable contract for frontend. |
| Security | Architecture | Chosen | All           | Dedicated DB user with minimum permissions, strong passwords, no public exposure for PostgreSQL. HTTPS for all traffic. Gemini API keys and DB credentials stored in backend environment variables. AI safety via prompt instructions and avoiding logging full prompts/answers. |
| Performance| Optimization | Chosen | All           | Frontend: Leverage Vercel CDN, basic code splitting if free. Backend: Sensible PostgreSQL indexes, efficient Gemini API calls, and streaming responses for perceived speed. Caching only if bottlenecks are identified. |

## Project Structure

```
himolde-study-friend/
├───frontend/                   # Vite + React (TypeScript) SPA
│   ├───src/                    # React components, logic, styles
│   │   ├───components/         # Reusable UI components (shadcn/ui based)
│   │   ├───pages/              # Main application pages (e.g., ChatPage)
│   │   ├───lib/                # Utility functions, API client, date/time utils
│   │   ├───assets/             # Images, fonts
│   │   ├───styles/             # Tailwind CSS config, global styles
│   │   ├───App.tsx             # Main React app component
│   │   ├───main.tsx            # Entry point
│   │   └───index.css           # Tailwind directives
│   ├───public/                 # Static assets
│   ├───tests/                  # Frontend tests (Vitest)
│   ├───.eslintrc.cjs           # ESLint configuration
│   ├───prettier.config.cjs     # Prettier configuration
│   ├───package.json            # Frontend dependencies
│   ├───tsconfig.json           # TypeScript configuration
│   ├───vite.config.ts          # Vite configuration
│   └───... (other frontend configs)
├───backend/                    # Python REST API
│   ├───src/                    # Python source code
│   │   ├───api/                # API endpoints and logic (e.g., chat, courses)
│   │   ├───services/           # Business logic (e.g., ChatService, KnowledgeBaseService)
│   │   ├───models/             # Pydantic models for request/response, DB models
│   │   ├───core/               # Shared utilities, config, logging setup
│   │   ├───db/                 # Database connection, schema, pgvector setup
│   │   ├───rag/                # RAG specific logic, Gemini API integration
│   │   ├───main.py             # Main application entry point
│   │   └───__init__.py
│   ├───tests/                  # Backend tests (Pytest)
│   ├───.env.example            # Environment variables example
│   ├───requirements.txt        # Python dependencies
│   ├───pyproject.toml          # Black, Flake8 configuration
│   ├───Dockerfile              # For Railway deployment
│   └───... (other backend configs)
├───docs/                       # Project documentation (including architecture.md, PRD, Epics, UX)
│   ├───architecture.md
│   ├───prd.md
│   ├───epics.md
│   ├───ux-design-specification.md
│   └───...
├───.github/                    # CI/CD workflows (GitHub Actions)
│   ├───workflows/
│   │   ├───frontend-ci.yml
│   │   └───backend-ci.yml
├───.gitignore
├───README.md
└───... (other root-level configs)
```

## Epic to Architecture Mapping

-   **Epic 1: Foundation & Core Chat Interface**
    -   Story 1.1: Project Initialization & CI/CD Pipeline Setup → `frontend/`, `backend/`, `.github/workflows/`
    -   Story 1.2: Design and Implement the Knowledge Base Schema → `backend/src/db/`, `backend/src/models/`
    -   Story 1.3: Build the Basic Chat Interface UI → `frontend/src/components/`, `frontend/src/pages/`
    -   Story 1.4: Implement Real-Time Message Handling in the UI → `frontend/src/lib/api-client.ts`, `backend/src/api/`

-   **Epic 2: Core Question Answering**
    -   Story 2.1: Implement Natural Language Query Input → `frontend/src/components/`, `backend/src/api/`
    -   Story 2.2: Implement Knowledge Base Retrieval → `backend/src/db/`, `backend/src/rag/`
    -   Story 2.3: Generate Conversational Responses → `backend/src/rag/`, `backend/src/api/`
    -   Story 2.4: Handle "I Don't Know" Scenarios → `backend/src/rag/`, `frontend/src/components/`

-   **Epic 3: User Feedback Loop**
    -   Story 3.1: Implement User Feedback Mechanism in UI → `frontend/src/components/`, `frontend/src/lib/api-client.ts`
    -   Story 3.2: Persist User Feedback → `backend/src/api/`, `backend/src/db/` (for feedback storage, if applicable)

## Technology Stack Details

### Core Technologies

-   **Frontend:**
    -   Vite: `^5.0.0` (Latest stable release `5.2.4` for optimal performance and features)
    -   React: `^18.2.0` (Current stable release)
    -   TypeScript: `^5.2.2` (Current stable release for enhanced type safety)
    -   Tailwind CSS: `^3.3.0` (Latest stable release `3.4.1` for utility-first styling)
    -   shadcn/ui: `~0.8.0` (As specified in UX Design Specification, aligns with Tailwind)
-   **Backend:**
    -   Python: `3.11.14` (Recommended stable version) / `3.12.2` (Latest stable version if available on Railway)
    -   FastAPI: `^0.122.0` (Latest stable release for high performance Python APIs)
    -   PostgreSQL: `^16.0` (Latest stable release)
    -   pgvector: `~0.5.0` (Compatible with PostgreSQL 16, for vector embeddings)
-   **AI:**
    -   Gemini API (Leveraging Google's latest multimodal models)

_Rationale: For frontend libraries, opting for the latest stable versions allows leveraging recent performance improvements, features, and better compatibility with modern development practices. For backend and database, stable and widely supported versions ensure robustness and access to recent features while maintaining compatibility with deployment platforms like Railway. Specific minor versions will be pinned in `package.json` and `requirements.txt` during implementation._

### Integration Points

-   **Frontend-Backend Communication:** REST API calls and streaming HTTP (SSE) via `frontend/src/lib/api-client.ts` to `backend/src/api/`.
-   **Backend-Database Communication:** Python ORM/library (e.g., SQLAlchemy) from `backend/src/db/` to PostgreSQL. `pgvector` will be used within PostgreSQL for vector search.
-   **Backend-Gemini API Communication:** Direct API calls from `backend/src/rag/` to Google's Gemini API endpoints.
-   **Backend Logging:** Console output primarily, collected by Railway.
-   **Frontend Asset Serving:** Vercel CDN serves static assets from `frontend/dist/`.

## Novel Pattern Designs

No entirely novel architectural patterns requiring bespoke design have been identified beyond the RAG architecture itself (which is integrated into the AI Application decision). The focus is on leveraging established best practices and components.

## Implementation Patterns

These patterns ensure consistent implementation across all AI agents:

-   **Naming Conventions:**
    -   **Frontend (React/TypeScript):**
        -   **React Components:** Use `PascalCase` (e.g., `ChatWindow`, `CourseCard`).
        -   **Variables/Functions:** Use `camelCase` (e.g., `userName`, `fetchData`).
        -   **Files:** Match the component name (e.g., `ChatWindow.tsx`).
    -   **Backend (Python):**
        -   **Variables/Functions:** Use `snake_case` (e.g., `user_name`, `fetch_data`).
        -   **Classes:** Use `PascalCase` (e.g., `CourseModel`, `ChatService`).
        -   **Files/Modules:** Use `snake_case` (e.g., `chat_api.py`).
    -   **PostgreSQL (Database):**
        -   **Table Names:** Use `snake_case` and `plural` (e.g., `courses`, `feedback`).
        -   **Column Names:** Use `snake_case` (e.g., `course_code`, `learning_outcomes`).
-   **Code Organization:**
    -   **Frontend (`frontend/src`):**
        -   Organize by **feature** for pages and major components (e.g., `pages/chat/`, `pages/courses/`).
        -   General reusable UI elements in `components/`.
        -   Utility functions and API client in `lib/`.
        -   Styles in `styles/`.
    -   **Backend (`backend/src`):**
        -   Organize by **type/domain** (e.g., `api/` for endpoints, `services/` for business logic, `db/` for database interactions, `rag/` for RAG logic).
    -   **Tests:**
        -   Frontend tests: co-located with the code they test (e.g., `ChatWindow.test.tsx` next to `ChatWindow.tsx`) or in a `__tests__` subdirectory.
        -   Backend tests: in a top-level `backend/tests/` directory, mirroring the `backend/src/` structure.
-   **Data Format (Consistency):**
    -   **API Responses (Success):** Always `200 OK` with JSON `{"data": ...}`.
    -   **API Responses (Error):** Non-2xx status with JSON `{ "error": "message", "code": "SOME_CODE" }`.
    -   **Chat Streaming:** SSE/HTTP where each chunk is JSON `{ "type": "chunk", "content": "..." }` and a final `{ "type": "done" }`.
    -   **Dates/Times:** Store and transmit as **UTC ISO-8601** strings.
-   **Communication:**
    -   **Frontend to Backend:** REST API calls and Server-Sent Events (SSE) / Streaming HTTP.
    -   **Backend to Database:** Python ORM/library to PostgreSQL.
    -   **Backend to Gemini API:** Direct HTTP requests to the Gemini API endpoints.
-   **Lifecycle (State Management):**
    -   **Frontend:** React's built-in state management (`useState`, `useReducer`, React Context) for UI state. Standard patterns for data fetching (loading, error, data states).
    -   **Backend:** Each API request handled as an independent operation.
-   **Location (Files & Configs):**
    -   **Configuration Files:** Place configuration files at the root of `frontend/` and `backend/` directories, or within a `core/` subdirectory for backend.
    -   **Environment Variables:** Use `.env` files in the `frontend/` and `backend/` roots for local development, and environment variables on Vercel/Railway for deployment.
    -   **Static Assets:** `frontend/public/`.
-   **Cross-cutting Concerns:** (See Consistency Rules below for details)

## Consistency Rules

### Naming Conventions

-   **Frontend (React/TypeScript):** React Components: `PascalCase`, Variables/Functions: `camelCase`, Files: Match component name.
-   **Backend (Python)::** Variables/Functions: `snake_case`, Classes: `PascalCase`, Files/Modules: `snake_case`.
-   **PostgreSQL (Database):** Table Names: `snake_case` (plural), Column Names: `snake_case`.

### Code Organization

-   **Frontend (`frontend/src`):** Organize by feature for pages/major components; reusable UI in `components/`; utilities/API client in `lib/`; styles in `styles/`.
-   **Backend (`backend/src`):** Organize by type/domain (e.g., `api/` for endpoints, `services/`, `db/`, `rag/`).
-   **Tests:** Frontend tests co-located or in `__tests__`; Backend tests in `backend/tests/`.

### Error Handling

-   **Frontend:** Error Boundaries for critical UI errors, inline messages/toast for network/backend issues.
-   **Backend:** Consistent HTTP status codes and JSON error objects (`{error: 'message', code: 'SOME_CODE'}`).

### Logging Strategy

-   Python's built-in `logging` module to console (DEBUG, INFO, WARNING, ERROR levels). Focus on key events; avoid secrets/API keys.

### Data Architecture

The core data architecture revolves around a PostgreSQL database. It will store structured course information, including:
-   `courses` table: `course_code` (primary key), `name`, `description`, `learning_outcomes`, `exam_format`, `mandatory_assignments`, etc.
-   `feedback` table: (if Epic 3 is implemented) `query`, `response`, `rating` (thumbs up/down), `timestamp`.
`pgvector` will be enabled in PostgreSQL to store vector embeddings for the RAG system, allowing semantic search over course content.

### API Contracts

API contracts will adhere to the REST API pattern.
-   **Main Chat Endpoint (`POST /chat`):** Streams responses using Server-Sent Events (SSE) / Streaming HTTP. Each chunk will be a JSON object: `{ "type": "chunk", "content": "..." }`, with a final `{ "type": "done" }`.
-   **Other Endpoints (e.g., `GET /courses`):** Return `200 OK` with a JSON object in the form `{"data": [...]}`.
-   **Error Responses:** Non-2xx HTTP status codes with a JSON object: `{ "error": "message", "code": "SOME_CODE" }`.
-   Specific endpoint paths (e.g., `POST /chat`, `GET /courses`) will be defined in the backend implementation.

### Security Architecture

As detailed in the Decision Summary, security focuses on dedicated PostgreSQL user with minimum permissions, HTTPS for all traffic, secure environment variable management for secrets (Gemini API keys, DB credentials), and AI safety via prompt instructions and filtering. No user authentication for the MVP.

### Performance Considerations

As detailed in the Decision Summary, performance optimization includes leveraging Vercel's CDN and basic code splitting for the frontend, and for the backend, sensible PostgreSQL indexing, efficient Gemini API calls, and reliance on streaming responses for perceived speed. Caching will be considered only if bottlenecks are identified post-MVP.

### Deployment Architecture

As detailed in the Decision Summary, the frontend (Vite React SPA) will be deployed on Vercel, and the backend service (Python REST API with PostgreSQL) will be deployed on Railway. This provides developer-friendly, managed hosting solutions.

## Development Environment

### Prerequisites

-   Node.js (for frontend)
-   Python (for backend)
-   Git
-   Docker (optional, for local PostgreSQL setup)

### Setup Commands

```bash
# Frontend setup
cd frontend
npm install
npm run dev

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Architecture Decision Records (ADRs)

(Key decisions from Decision Summary will be formalized into ADRs as needed)

---

_Generated by BMAD Decision Architecture Workflow v1.0_
_Date: {{date}}_
_For: {{user_name}}_

## Validation Summary

### Document Quality Score

- Architecture Completeness: Complete
- Version Specificity: Mostly Complete
- Pattern Clarity: Crystal Clear
- AI Agent Readiness: Ready

### Critical Issues Found

- N/A

### Recommended Actions Before Implementation

- Final review of `architecture.md` to ensure all `{{placeholders}}` have been replaced with concrete information.