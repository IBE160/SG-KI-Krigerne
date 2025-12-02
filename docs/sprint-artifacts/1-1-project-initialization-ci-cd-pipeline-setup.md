# Story 1.1: Project Initialization & CI/CD Pipeline Setup

Status: ready-for-dev

## Story

As a **Developer**,
I want **a standardized project structure and an automated CI/CD pipeline**,
So that **I can ensure consistent development practices and reliable deployments**.

## Acceptance Criteria

1.  **Given** a new project is needed,
2.  **When** the initialization script is run,
3.  **Then** a standard folder structure (e.g., `src`, `docs`, `tests`) is created.
4.  **And** a `package.json` (or equivalent) with core dependencies (e.g., a web framework, test runner) is created.
5.  **And** a basic "Hello World" version of the app can be run locally.
6.  **And** a CI/CD pipeline (e.g., GitHub Actions) is configured to automatically run linters and basic tests on every push.

## Requirements Context Summary

### From Epics (docs/epics.md):
- **User Story:** As a Developer, I want a standardized project structure and an automated CI/CD pipeline, so that I can ensure consistent development practices and reliable deployments.
- **Acceptance Criteria:** (See above)
- **Technical Notes:** Use Vite for the React frontend and Vitest for testing. Set up basic linting with ESLint. The CI/CD pipeline should use GitHub Actions.

### From Architecture (docs/architecture.md):
- **Project Initialization:** The project will use Vite + React (TypeScript) frontend, integrated with Tailwind CSS and shadcn/ui.
- **Initialization Commands:** Specific `npm` commands are provided for creating the Vite project, navigating, installing dependencies, installing Tailwind CSS, initializing Tailwind/PostCSS, installing `@types/node`, and initializing shadcn/ui.
- **Architectural Decisions:**
    - **Language/TypeScript:** TypeScript for type safety.
    - **Styling Solution:** Tailwind CSS and shadcn/ui.
    - **Testing Framework:** Vitest.
    - **Linting/Formatting:** ESLint and Prettier.
    - **Build Tooling:** Vite and Rollup.
    - **Project Structure:** Vite default project structure.
- **CI/CD:** Configuration in `.github/workflows/`.

## Dev Notes

- Relevant architecture patterns and constraints
- Source tree components to touch
- Testing standards summary

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- Cite all technical details with source paths and sections, e.g. [Source: docs/<file>.md#Section]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/epic-1/stories/1-1/1-1-project-initialization-ci-cd-pipeline-setup.context.xml

### Agent Model Used

Gemini 1.5 Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log

- YYYY-MM-DD - [Your Name/Alias] - Initial draft based on PRD and Architecture.

## Tasks / Subtasks

- [ ] **Initialize Frontend Project (AC: 1, 2, 3, 4, 5)**
  - [ ] Create Vite + React (TypeScript) project: `npm create vite@latest himolde-study-friend -- --template react-ts` [Source: docs/architecture.md#Project-Initialization]
  - [ ] Navigate into frontend directory: `cd himolde-study-friend` [Source: docs/architecture.md#Project-Initialization]
  - [ ] Install frontend dependencies: `npm install` [Source: docs/architecture.md#Project-Initialization]
  - [ ] Install Tailwind CSS and peer dependencies: `npm install -D tailwindcss postcss autoprefixer` [Source: docs/architecture.md#Project-Initialization]
  - [ ] Initialize Tailwind CSS and PostCSS: `npx tailwindcss init -p` [Source: docs/architecture.md#Project-Initialization]
  - [ ] Install `@types/node` for path resolution: `npm install -D @types/node` [Source: docs/architecture.md#Project-Initialization]
  - [ ] Initialize shadcn/ui: `npx shadcn-ui@latest init` [Source: docs/architecture.md#Project-Initialization]
  - [ ] Verify "Hello World" application runs locally.
- [ ] **Setup Linting and Formatting (AC: 6)**
  - [ ] Integrate ESLint for frontend code quality. [Source: docs/epics.md#Story-1.1, docs/architecture.md#Decision-Summary]
  - [ ] Integrate Prettier for frontend code formatting. [Source: docs/architecture.md#Decision-Summary]
- [ ] **Setup Testing Framework (AC: 6)**
  - [ ] Integrate Vitest for frontend testing. [Source: docs/epics.md#Story-1.1, docs/architecture.md#Decision-Summary]
  - [ ] Create a basic example test to confirm setup.
- [ ] **Configure CI/CD Pipeline (AC: 6)**
  - [ ] Create `.github/workflows/frontend-ci.yml` for frontend. [Source: docs/architecture.md#Epic-to-Architecture-Mapping]
  - [ ] Configure workflow to run linters on push.
  - [ ] Configure workflow to run tests on push.
  - [ ] Ensure pipeline triggers and passes for basic changes.
- [ ] **Documentation and Project Structure Verification (AC: 1, 3)**
  - [ ] Verify adherence to Vite default project structure. [Source: docs/architecture.md#Project-Structure]
  - [ ] Confirm `package.json` contains core dependencies as outlined in architecture. [Source: docs/architecture.md#Technology-Stack-Details]

### Structure Alignment Summary

Given this is the first story, there are no previous story learnings or an existing `unified-project-structure.md` to align with. The primary project structure is derived directly from the architectural decisions for a Vite + React (TypeScript) frontend and a Python backend, as detailed in `docs/architecture.md`.

**Key Project Structure Elements:**
- **Frontend:** `himolde-study-friend/frontend/`
    - `src/`: React components, logic, styles
    - `components/`: Reusable UI components (shadcn/ui based)
    - `pages/`: Main application pages
    - `lib/`: Utility functions, API client
    - `assets/`: Images, fonts
    - `styles/`: Tailwind CSS config, global styles
    - `App.tsx`, `main.tsx`, `index.css`
    - `public/`: Static assets
    - `tests/`: Frontend tests (Vitest)
    - `.eslintrc.cjs`, `prettier.config.cjs`, `package.json`, `tsconfig.json`, `vite.config.ts`
- **Backend:** `himolde-study-friend/backend/`
    - `src/`: Python source code
    - `api/`: API endpoints
    - `services/`: Business logic
    - `models/`: Pydantic models
    - `core/`: Shared utilities, config, logging
    - `db/`: Database connection
    - `rag/`: RAG specific logic
    - `main.py`
    - `tests/`: Backend tests (Pytest)
    - `requirements.txt`, `pyproject.toml`, `Dockerfile`
- **Docs:** `docs/` (Project documentation)
- **CI/CD:** `.github/workflows/`

This story focuses on establishing the basic Vite + React project structure and initial CI/CD setup, forming the foundation for subsequent development. All development within this story should align with the structure defined in `docs/architecture.md`. No conflicts or variances are expected at this initial stage.

## Dev Notes

-   **Relevant architecture patterns and constraints:**
    -   Frontend: Vite + React (TypeScript) [Source: docs/architecture.md#Executive-Summary]
    -   Styling: Tailwind CSS + shadcn/ui [Source: docs/architecture.md#Executive-Summary]
    -   Testing: Vitest (Frontend), Pytest (Backend - not in this story scope but good to note) [Source: docs/architecture.md#Decision-Summary]
    -   Linting/Formatting: ESLint + Prettier (Frontend), Black + Flake8 (Backend - not in this story scope) [Source: docs/architecture.md#Decision-Summary]
    -   Build Tooling: Vite/Rollup [Source: docs/architecture.md#Decision-Summary]
    -   Project Structure: Vite default for frontend, Python domain-based for backend [Source: docs/architecture.md#Project-Structure]
    -   CI/CD: GitHub Actions for automation [Source: docs/epics.md#Story-1.1]

-   **Source tree components to touch:**
    -   `himolde-study-friend/frontend/` (new project directory)
    -   `himolde-study-friend/frontend/package.json` (for dependencies)
    -   `himolde-study-friend/frontend/tailwind.config.cjs` (for Tailwind setup)
    -   `himolde-study-friend/frontend/src/App.tsx`, `main.tsx` (for "Hello World")
    -   `.github/workflows/frontend-ci.yml` (for CI/CD configuration)

-   **Testing standards summary:**
    -   Frontend testing will utilize Vitest, following modern JavaScript/TypeScript testing practices. Initial setup will involve basic unit tests for the "Hello World" component.
    -   CI/CD pipeline will automatically run linters and tests, ensuring code quality and preventing regressions.

### Project Structure Notes

-   **Alignment with unified project structure (paths, modules, naming):** This story establishes the initial project structure, which will align with the `himolde-study-friend/frontend/` and `himolde-study-friend/backend/` layout outlined in `docs/architecture.md`. Naming conventions (PascalCase for components, camelCase for functions in JS/TS) will be adhered to from the outset.
-   **Detected conflicts or variances (with rationale):** None are anticipated at this foundational stage, as this story is defining the initial structure based on pre-approved architectural decisions.

### References

-   [Source: docs/epics.md#Epic-1:-Foundation-&-Core-Chat-Interface]
-   [Source: docs/architecture.md#Project-Initialization]
-   [Source: docs/architecture.md#Decision-Summary]
-   [Source: docs/architecture.md#Project-Structure]

### Learnings from Previous Story

**From Story None (Status: First story in epic - no predecessor context)**

-   No previous story to learn from. This story sets the foundation.