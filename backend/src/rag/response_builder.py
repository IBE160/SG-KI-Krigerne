from typing import Any, Dict, Optional

from backend.src.rag.query_parser import ParsedQuery


def build_response(parsed: ParsedQuery, kb_result: Optional[Dict[str, Any]]) -> str:
    """
    Turn a parsed query + raw knowledge into a friendly answer string.
    """

    # 1) No course info found
    if kb_result is None:
        # We know the course code, but it wasn't in the knowledge base
        if parsed.course_code:
            return (
                f"I'm sorry, I couldn't find information for the course "
                f"{parsed.course_code}. You may want to double-check the course "
                f"code or visit the official HiMolde course pages."
            )

        # We don't even know which course
        return (
            "I couldn't figure out which course you're asking about. "
            "Try including a course code like ADM120 or MAT100 in your question.\n\n"
            "For example: “What is the exam format for ADM120?”"
        )

    # 2) We have data for a specific course
    code = kb_result.get("course_code")
    name = kb_result.get("name")
    field = kb_result.get("field")
    value = (kb_result.get("value") or "").strip()

    course_label = f"{code}" if not name else f"{code} ({name})"

    # Specific intents
    if parsed.intent == "get_exam_format":
        return (
            f"For {course_label}, the exam format is:\n\n"
            f"{value}\n\n"
            "If you'd like, you can also ask about learning outcomes or "
            "mandatory assignments for this course."
        )

    if parsed.intent == "get_learning_outcomes":
        return (
            f"The main learning outcomes for {course_label} are:\n\n"
            f"{value}\n\n"
            "As you read them, think about which of these feel new to you – "
            "that’s where you’ll want to spend extra study time."
        )

    if parsed.intent == "get_mandatory_assignments":
        return (
            f"Here is what I found about mandatory assignments in {course_label}:\n\n"
            f"{value}\n\n"
            "Make sure you plan your semester so you can submit all mandatory "
            "work on time – missing them can prevent you from taking the exam."
        )

    if field == "overview":
        return (
            f"Here is a quick overview of {course_label}:\n\n"
            f"{value}\n\n"
            "If you want details about one of these specifically, you can ask "
            'something like “What is the exam format for '
            f'{code}?” or “What are the learning outcomes for {code}?”'
        )

    # Generic fallback if we don't recognize the intent for some reason
    if value:
        return (
            f"Here is some information I found for {course_label}:\n\n"
            f"{value}"
        )

    # Last-ditch answer
    return (
        "I found the course in the knowledge base, but there wasn't any useful "
        "text to show. You may want to check the official course description."
    )
