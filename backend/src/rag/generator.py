from typing import Optional
from src.rag.query_parser import ParsedQuery

# A mapping from intent to a user-friendly description of the information type
INTENT_TO_FRIENDLY_NAME = {
    "get_learning_outcomes": "learning outcomes",
    "get_exam_format": "exam format",
    "get_mandatory_assignments": "mandatory assignments",
}

def generate_response(parsed_query: ParsedQuery, retrieved_information: Optional[str]) -> str:
    """
    Generates a conversational response based on the parsed query and retrieved information.

    Args:
        parsed_query: The parsed query containing intent and entities.
        retrieved_information: The information retrieved from the knowledge base (a string),
                               or None if no information was found.

    Returns:
        A natural language conversational response.
    """
    course_code = parsed_query.course_code.upper() if parsed_query.course_code else "the specified course"

    if retrieved_information is None:
        information_type = INTENT_TO_FRIENDLY_NAME.get(parsed_query.intent, "the requested information")
        return f"I'm sorry, I couldn't find information about the {information_type} for {course_code}."

    if parsed_query.intent == "get_learning_outcomes":
        return f"The learning outcomes for {course_code} are: {retrieved_information}"
    elif parsed_query.intent == "get_exam_format":
        return f"The exam format for {course_code} is: {retrieved_information}"
    elif parsed_query.intent == "get_mandatory_assignments":
        return f"The mandatory assignments for {course_code} are: {retrieved_information}"
    else:
        # Fallback for unexpected intents, though query_parser should prevent this in most cases
        return f"Here is some information about {course_code}: {retrieved_information}"

