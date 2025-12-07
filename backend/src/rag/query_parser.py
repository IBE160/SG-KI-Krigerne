from dataclasses import dataclass
import re
from typing import List, Dict, Optional

# What we’ll pass around inside the backend
@dataclass
class ParsedQuery:
    raw_query: str
    course_code: Optional[str] = None
    intent: Optional[str] = None


# Example: ADM120, MAT100, IBE210, etc.
COURSE_CODE_RE = re.compile(r"\b([A-Z]{2,5}\d{3})\b", re.IGNORECASE)

INTENT_KEYWORDS = {
    "get_learning_outcomes": [
        "learning outcome",
        "learning outcomes",
        "what will i learn",
        "what do i learn",
        "læringsutbytte",
    ],
    "get_exam_format": [
        "exam format",
        "how is the exam",
        "how is the final",
        "assessment",
        "eksamen",
        "exam type",
    ],
    "get_mandatory_assignments": [
        "mandatory assignment",
        "mandatory assignments",
        "mandatory work",
        "oblig",
        "obligatory",
        "work requirement",
        "obligatory assignment",
    ],
    # generic “tell me about this course”
    "course_overview": [
        "tell me about",
        "overview",
        "what is",
        "information about",
        "info about",
        "what can you tell me",
        "give me details",
    ],
}


def parse_query(
        query: str,
        history: Optional[List[Dict[str, str]]] = None,
        ) -> ParsedQuery:
    """
    Try to extract a course code and an intent from the user’s query.
    """
    lower = query.lower()

    # 1) course code, if any
    course_match = COURSE_CODE_RE.search(query)
    course_code = course_match.group(1).upper() if course_match else None

    # 2) intent
    intent: Optional[str] = None
    for candidate_intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            intent = candidate_intent
            break

    # 3) sensible fallback: if we have a course but no specific intent,
    #    treat it as "tell me about this course"
    if course_code and intent is None:
        intent = "course_overview"

    return ParsedQuery(raw_query=query, course_code=course_code, intent=intent)
