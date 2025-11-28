# Brainstorming Session Results

**Session Date:** 2025-11-13
**Facilitator:** Strategic Business Analyst Mary
**Participant:** BIP

## Executive Summary

**Topic:** User Problems and Pain Points for Himolde Study Friend Chatbot

**Session Goals:** To understand user problems and pain points, identify benefits, risks, and generate creative solutions for the Himolde Study Friend chatbot.

**Techniques Used:** Six Thinking Hats, Question Storming

**Total Ideas Generated:** Approximately 40 distinct ideas/points (across Green Hat and Question Storming)

### Key Themes Identified:

-   Information scattering and its negative impact on students and staff.
-   The potential of a chatbot to centralize information and improve efficiency.
-   The critical importance of data accuracy and maintenance.
-   The need for careful scope management and user expectation setting.
-   Opportunities for innovative features and long-term scalability.

## Technique Sessions

### Six Thinking Hats

#### White Hat (Facts)
-   Information scattered across multiple systems (Canvas, catalogs, emails).
-   Students spend significant time locating course details, leading to frustration.
-   Staff receive repetitive questions.
-   No unified data source.
-   Students frequently need basic info (learning outcomes, exam format, mandatory assignments).

#### Red Hat (Emotions)
-   Frustration, annoyance, irritation, feeling "fed up."
-   Overwhelmed, mentally drained, overloaded, stressed.
-   Uncertainty, insecurity (about exam format, assignments, preparedness).
-   Time pressure, anxiety from lost time and approaching deadlines.
-   Annoyance/guilt about asking teachers for "simple" things.
-   Feeling disconnected/unsupported by existing systems, disorganization, lack of prioritization.
-   Short-lived relief when information is found, knowing the struggle will repeat.

#### Yellow Hat (Benefits)
-   Students save significant time (more for studying/personal life, reduced stress).
-   Reduced frustration leading to a better student experience (smoother workflow, confidence, support).
-   More accurate and consistent information for everyone (reduced miscommunication, misunderstandings).
-   Teachers and admin staff get fewer repetitive questions (more time for teaching/feedback, less burnout).
-   Chatbot becomes a foundation for expansion (personalized reminders, study planning, analytics, API integration).
-   Improved student confidence and academic success (better preparation, control over studies).
-   A scalable solution that can help future students automatically (new, exchange, returning students).
-   Opportunity to modernize the university’s digital experience (inspire more tech, position as innovative).

#### Black Hat (Risks)
-   Incorrect/misleading information (AI misinterpretation, outdated data, formatting issues).
-   Manual knowledge base maintenance (stale data, ongoing effort).
-   Limited scope might disappoint users (unmet expectations for personalized guidance, live integration).
-   Users may test with unexpected/complex questions (outside KB, cross-course).
-   AI hallucination risk (fabrication, incorrect answers).
-   Performance and technical complexity (Gemini CLI, BMaD, prompt strategy, interface, latency).
-   Hard to ensure consistent quality across all courses (varying detail, inconsistent formats).
-   Potential privacy or ethical concerns (accidental personal data entry, disclaimers, misuse).
-   Adoption risk (students forget, prefer teachers, not linked, feels experimental).
-   Time constraints (insufficient time for polish, incomplete features, rushed testing).

#### Green Hat (Ideas/Solutions)
-   Semi-automated data collection tool (scraper/parser for public catalog).
-   “I’m not sure” fallback mode (show direct text from KB when confidence is low).
-   Smart question rewriting (internally rewrite user query into structured query).
-   User feedback loop (👍/👎 to log incorrect responses, add data, adjust prompts).
-   Course-profile cards (visual summary of exam format, assignments, outcomes).
-   Support “student workflows” (compare courses, summarize exam formats).
-   Build modular RAG architecture for easy future upgrades (retriever, prompt builder, LLM responder).
-   “Teacher Mode” for staff (check student view, verify info, edit data).
-   Automated “diff checker” for course updates (compare old vs new, alert changes).
-   Course info extraction using LLMs (paste description, extract structured fields).
-   Gamify adoption (streaks, "You saved X minutes!").
-   Deploy in places students already live (Canvas LTI, Discord, VS Code extension).
-   Keep an offline fallback dataset (search local JSON if AI fails).
-   Multi-turn reasoning for clarity (ask follow-up questions for ambiguous queries).

### Question Storming

#### Questions about Users & Problems
-   How do students currently search for course information, step by step?
-   Which parts of the search process cause the most frustration?
-   Are first-year students struggling more than advanced students?
-   What information do students check most frequently?
-   What questions do students repeatedly ask teachers?
-   How do international students experience the current information system?
-   What expectations do students have for a “study assistant” chatbot?

#### Questions about Data & Accuracy
-   Where will our initial course information come from?
-   How will we ensure the data is complete and correct?
-   How often does course data change, and who updates it?
-   What should the chatbot do if information is missing?
-   What fields are essential (exam format, assignments, outcomes)?
-   How do we prevent hallucination or misinformation?
-   Should we store the raw course text or only extracted fields?

#### Questions about Technical Implementation
-   How will we structure the knowledge base (JSON, CSV, database)?
-   What is the best architecture using Gemini + BMaD for retrieval?
-   How will the chatbot select the correct course when multiple exist?
-   What interface should we build first (terminal/web/Discord)?
-   Do we need a query rewriting step before retrieval?
-   How do we log user queries for debugging?
-   Should we support multi-turn conversations or only single questions?

#### Questions about UX & Interaction
-   What should a typical answer look like?
-   Should the bot show the source of the information?
-   How do we make the bot sound trustworthy and clear?
-   Should the bot ask follow-up questions when unclear?
-   How fast do users expect the bot to respond?
-   Should the bot support comparing two courses?

#### Questions about Risks & Mitigation
-   What happens if students rely on incorrect information?
-   How can we build a safety fallback when the bot isn’t confident?
-   What if the knowledge base becomes outdated?
-   What mistakes might students make when asking questions?
-   How do we detect ambiguous questions?

#### Questions about Opportunities
-   Could this evolve into a full student assistant?
-   Can teachers use the system to ensure consistency?
-   Could the system help new students understand course structures?
-   Is there potential for analytics (most asked questions)?
-   Can we scale to all courses later, or integrate with APIs?

#### Questions about MVP Scope & Feasibility
-   How many courses should the MVP support?
-   What is “good enough” accuracy for the MVP?
-   What absolutely must be included vs. what can wait?
-   What can we realistically complete within the course timeline?

#### Questions about Evaluation & Testing
-   How will we test the chatbot’s accuracy?
-   What metrics should we measure (precision, coverage, speed)?
-   How do we simulate real student questions?
-   How many test cases do we need?

#### Questions about Maintenance & Long-Term Use
-   Who will update the data after the semester?
-   How can we make the system easy to update?
-   What happens if the university changes course formats?

#### Meta / Reflection Questions
-   What assumptions are we making about student behavior?
-   What blind spots do we have?
-   What questions are we not asking yet that we should ask?

## Action Planning

### Top 3 Priority Ideas

#### #1 Priority: Define the MVP Knowledge Base
- Rationale: This is the foundational step. Without a clear definition of what data the chatbot will handle, we cannot proceed with architecture or implementation. It directly addresses the "Data & Accuracy" risk.
- Next steps:
    1. Choose 5-10 initial courses.
    2. Decide on essential fields (exam type, mandatory assignments, learning outcomes).
    3. Create JSON/CSV templates for structured data.
- Resources needed: Course catalogs, project team.
- Timeline: 1-2 days.

#### #2 Priority: Build the Data-Gathering Workflow
- Rationale: Directly tackles the "manual knowledge base maintenance" risk. Even semi-automation will significantly improve efficiency and data consistency.
- Next steps:
    1. Pick a method: manual copy/paste, semi-automated scraper, or LLM-assisted extraction.
    2. Implement the chosen method.
    3. Start populating the structured dataset for the MVP courses.
- Resources needed: Project team, potentially web scraping tools or LLM access.
- Timeline: 2-3 days.

#### #3 Priority: Design the Core Architecture
- Rationale: A modular and well-thought-out architecture is crucial for scalability, reducing hallucination risk, and ensuring reliable output. It addresses "Technical Implementation" and "AI hallucination" risks.
- Next steps:
    1. Focus on retrieval function (how the bot finds info in KB).
    2. Design the prompt template (how user query is framed for LLM).
    3. Define output formatting (how the bot presents answers).
    4. Plan fallback and error handling mechanisms.
- Resources needed: Project team, knowledge of RAG/LLM architecture.
- Timeline: 2-3 days.

## Reflection and Follow-up

### What Worked Well
-   The "Six Thinking Hats" provided a structured way to explore the problem from multiple perspectives (facts, emotions, benefits, risks, solutions).
-   "Question Storming" generated a comprehensive list of inquiries, ensuring we consider many angles before jumping to solutions.
-   The collaborative nature of the session allowed for a rich exchange of ideas and concerns.

### Areas for Further Exploration
-   Deeper dive into specific technical challenges of integrating Gemini CLI with BMaD.
-   Detailed analysis of existing university systems for course information to better inform data gathering.
-   User research to validate assumptions about student behavior and expectations.

### Recommended Follow-up Techniques
-   **Mind Mapping:** To visually organize the vast amount of questions and ideas generated.
-   **SCAMPER Method:** To further refine and innovate on the Green Hat ideas.

### Questions That Emerged
-   All questions from the "Question Storming" section are still valid and require answers as we progress.

### Next Session Planning
-   **Suggested topics:** Detailed technical design for MVP, knowledge base structure, user interface options.
-   **Recommended timeframe:** Within the next week.
-   **Preparation needed:** Research into RAG architectures, data structuring best practices, and available UI frameworks.

---

_Session facilitated using the BMAD CIS brainstorming framework_
