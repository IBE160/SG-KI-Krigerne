import re
from pydantic import BaseModel
from typing import Optional, Literal

class ParsedQuery(BaseModel):
    intent: Optional[Literal["get_exam_format", "get_learning_outcomes", "get_mandatory_assignments"]] = None
    course_code: Optional[str] = None

def parse_query(query: str) -> ParsedQuery:
    """
    Parses a natural language query to extract intent and entities.
    """
    query = query.lower()
    parsed_result = ParsedQuery()

    # Intent detection
    if "exam" in query:
        parsed_result.intent = "get_exam_format"
    elif "learning outcome" in query or "learning outcomes" in query:
        parsed_result.intent = "get_learning_outcomes"
    elif "mandatory assignment" in query or "mandatory assignments" in query:
        parsed_result.intent = "get_mandatory_assignments"

    # Entity extraction (course code)
    # This regex is a simple example and might need to be improved
    match = re.search(r"\b([a-z]{2,3}\d{3,4})\b", query)
    if match:
        parsed_result.course_code = match.group(1).upper()

    return parsed_result
