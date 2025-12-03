from typing import Any, Dict, List, Optional
from pathlib import Path

from src.models.course import Course
from src.db.knowledge_base_manager import load_knowledge_base
from src.rag.query_parser import ParsedQuery

# A mapping from intent to the attribute on the Course model
INTENT_TO_ATTRIBUTE = {
    "get_learning_outcomes": "learning_outcomes",
    "get_exam_format": "exam_format",
    "get_mandatory_assignments": "mandatory_assignments",
}


def retrieve_knowledge(
    parsed_query: ParsedQuery, knowledge_base: List[Course]
) -> Optional[str]:
    """
    Retrieves specific information from the knowledge base based on the parsed query.

    Args:
        parsed_query: The parsed query containing intent and entities.
        knowledge_base: The list of courses loaded from the knowledge base.

    Returns:
        The requested information as a string, or None if not found.
    """
    if not parsed_query.course_code:
        return None

    course_code = parsed_query.course_code.upper()
    target_course = next(
        (course for course in knowledge_base if course.course_code.upper() == course_code),
        None,
    )

    if not target_course:
        return None

    attribute = INTENT_TO_ATTRIBUTE.get(parsed_query.intent)
    if not attribute:
        return None

    retrieved_info = getattr(target_course, attribute, None)

    return str(retrieved_info) if retrieved_info is not None else None
