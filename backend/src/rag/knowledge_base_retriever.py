from typing import Any, Dict, List, Optional

from backend.src.models.course import Course
from backend.src.rag.query_parser import ParsedQuery

# Which Course attribute each intent maps to.
# None means: "give me an overview using multiple fields"
INTENT_TO_ATTRIBUTE = {
    "get_learning_outcomes": "learning_outcomes",
    "get_exam_format": "exam_format",
    "get_mandatory_assignments": "mandatory_assignments",
    "course_overview": None,
}


def _find_course(course_code: str, knowledge_base: List[Course]) -> Optional[Course]:
    code_upper = course_code.upper()
    return next(
        (c for c in knowledge_base if c.course_code.upper() == code_upper),
        None,
    )


def retrieve_knowledge(
    parsed_query: ParsedQuery, knowledge_base: List[Course]
) -> Optional[Dict[str, Any]]:
    """
    Look up relevant information in the knowledge base.

    Returns a dict like:
    {
        "course_code": "ADM120",
        "name": "Marketing",
        "field": "exam_format" | "learning_outcomes" | "mandatory_assignments" | "overview",
        "value": "...",            # string or combined string for overview
    }
    or None if nothing useful is found.
    """
    if not parsed_query.course_code:
        return None

    course = _find_course(parsed_query.course_code, knowledge_base)
    if not course:
        return None

    attribute = INTENT_TO_ATTRIBUTE.get(parsed_query.intent)

    # 1) Full overview
    if attribute is None:
        parts = []

        if course.learning_outcomes:
            parts.append(
                f"• Learning outcomes: {course.learning_outcomes.strip()}"
            )
        if course.exam_format:
            parts.append(f"• Exam format: {course.exam_format.strip()}")
        if course.mandatory_assignments:
            parts.append(
                f"• Mandatory assignments: {course.mandatory_assignments.strip()}"
            )

        if not parts:
            return None

        return {
            "course_code": course.course_code,
            "name": course.name,
            "field": "overview",
            "value": "\n".join(parts),
        }

    # 2) Single attribute
    value = getattr(course, attribute, None)
    if value is None:
        return None

    return {
        "course_code": course.course_code,
        "name": course.name,
        "field": attribute,
        "value": str(value),
    }
