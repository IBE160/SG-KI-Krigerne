# Proposal: Himolde Study Friend

## 1. Problem Statement
Students often spend unnecessary time searching for basic course information such as learning outcomes, exam format, and mandatory assignments. This information is spread across multiple systems (Canvas, course catalogs, or emails), making it time-consuming and frustrating to find.  

We want to simplify this process by letting students ask a chatbot directly and get accurate answers instantly.

---

## 2. Goal / Solution
Develop an AI-powered chatbot that allows students to quickly retrieve course information by entering the course name or code and asking natural language questions.  
The chatbot will draw from a structured **knowledge base** containing official course data and respond in clear, conversational language.

---

## 3. Users
- **Primary user:** Students at the university who want quick access to course information.  
- **Secondary user:** Administrative staff or teachers who may want to verify what information students are seeing.

---

## 4. Value Proposition
- Saves time and frustration for students.
- Ensures consistent and accurate information.
- Reduces the number of repetitive questions sent to course staff.
- Serves as a foundation for future expansion (e.g., personalized study reminders or Q&A about deadlines).

---

## 5. Scope (for MVP)
### In Scope
- Chatbot that can answer questions like:
  - “What are the learning outcomes for INF100?”
  - “Does PSY201 have an oral exam?”
  - “Are there any mandatory assignments in DAT110?”
- Basic web or chat interface for testing.
- Backend connection to a structured dataset or knowledge base (manual JSON or CSV is fine for MVP).

### Out of Scope (for now)
- Integration with official university APIs or live systems.
- User authentication or personalized dashboards.
- Support for multiple languages.

---

## 6. Success Criteria (MVP)
- [ ] A working chatbot that can correctly answer at least 80 % of a fixed set of test questions about known courses.  
- [ ] Users can interact via a simple interface (console, web chat, or VS Code terminal).  
- [ ] Answers come from a structured data source (not hardcoded).  
- [ ] The project is documented and demonstrated at the end of the course.

---

## 7. Risks and Mitigation
| Risk | Impact | Mitigation |
|------|---------|-------------|
| Data availability (course info not in one place) | High | Build a small local knowledge base manually for demo purposes. |
| AI accuracy | Medium | Use controlled prompt templates and limit scope of questions. |
| Time constraints | Medium | Focus on core chatbot → skip interface polish if needed. |
| Integration complexity | Low | Keep architecture modular for future expansion. |

---

## 8. Timeline (draft)
| Phase | Focus | Output |
|-------|--------|---------|
| Phase 1–2 | Analysis + Planning | `proposal.md`, `product-brief.md`, `PRD.md` |
| Phase 3 | Solution architecture | Prompt design, data structure, API plan |
| Phase 4 | Implementation | Working chatbot MVP |
| Phase 5 | Final polish + presentation | Documented and demo-ready app |

---

## 9. References / Inspiration
- University course catalogs and Canvas pages.
- OpenAI / Gemini / RAG (Retrieval-Augmented Generation) examples for Q&A bots.
- Suggested project proposals from teachers

## 10. Supporting Documents (Brainstorm and research)

## Brainstorming Sessions

- [Brainstorming session - Six thinking hats](docs/brainstorming-session-results-2025-11-13.md)

- [Brainstorming session - Scamper Analysis](docs/SCAMPER_ANALYSIS.md)

## Research Sessions

- [Research - How students find information](docs/research-user-2025-11-13.md)

