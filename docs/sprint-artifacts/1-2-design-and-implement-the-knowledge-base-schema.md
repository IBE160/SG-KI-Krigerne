# Story 1.2: Design and Implement the Knowledge Base Schema

Status: drafted

## Story

As a System,
I want a well-defined and structured knowledge base schema,
so that course information can be stored accurately and retrieved efficiently.

## Acceptance Criteria

1.  **Given** course data needs to be stored,
2.  **When** the knowledge base is created,
3.  **Then** a JSON file (`knowledge_base.json`) is created with a clear schema.
4.  **And** the schema supports fields for `course_code`, `learning_outcomes`, `exam_format`, and `mandatory_assignments`.
5.  **And** the system can programmatically load and parse this JSON file without errors.
6.  **And** an initial dummy course is added to the file for testing purposes.
7.  **And** file permissions are set to prevent unauthorized modification of the knowledge base.

## Tasks / Subtasks

- [ ] Task 1: Define `knowledge_base.json` schema (AC: 3, 4)
  - [ ] Subtask 1.1: Create `knowledge_base.json` in `backend/src/db/`
  - [ ] Subtask 1.2: Define fields for `course_code`, `learning_outcomes`, `exam_format`, `mandatory_assignments`
- [ ] Task 2: Implement knowledge base creation and loading (AC: 2, 5)
  - [ ] Subtask 2.1: Write script/function to create `knowledge_base.json` if it doesn't exist
  - [ ] Subtask 2.2: Implement logic to load and parse `knowledge_base.json`
  - [ ] Subtask 2.3: Add error handling for JSON parsing
- [ ] Task 3: Add initial dummy course (AC: 6)
  - [ ] Subtask 3.1: Add a dummy course entry to `knowledge_base.json`
- [ ] Task 4: Set file permissions (AC: 7)
  - [ ] Subtask 4.1: Research appropriate file permissions for `knowledge_base.json` to prevent unauthorized modification
  - [ ] Subtask 4.2: Implement file permission setting in the creation script/deployment process
- [ ] Task 5: Write unit/integration tests
  - [ ] Subtask 5.1: Test schema validity
  - [ ] Subtask 5.2: Test loading and parsing of `knowledge_base.json`
  - [ ] Subtask 5.3: Test handling of invalid JSON
  - [ ] Subtask 5.4: Test retrieval of dummy course data

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - Data Persistence: PostgreSQL is chosen for structured, relational course data. The initial knowledge base will be a JSON file, anticipating future migration to PostgreSQL for scalability and advanced features like `pgvector`.
  - Project Structure: `backend/src/db/` for database-related code, `backend/src/models/` for defining data models.
- **Source tree components to touch:**
  - `backend/src/db/` (for `knowledge_base.json` creation/access logic and eventual PostgreSQL integration)
  - `backend/src/models/` (for defining schema/structure for course data, e.g., Pydantic models for JSON or ORM models for PostgreSQL)
- **Testing standards summary:**
  - Pytest for backend unit and integration tests.

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)
- Detected conflicts or variances (with rationale)

### References

- [Source: docs/epics.md#Story 1.2: Design and Implement the Knowledge Base Schema (MVP)]
- [Source: docs/architecture.md#Decision Summary]
- [Source: docs/architecture.md#Project Structure]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
