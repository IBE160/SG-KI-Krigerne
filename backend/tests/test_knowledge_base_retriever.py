import pytest
from typing import List, Optional
from pathlib import Path

from backend.src.models.course import Course
from backend.src.rag.query_parser import ParsedQuery
from backend.src.rag.knowledge_base_retriever import retrieve_knowledge

# Sample course data for testing
SAMPLE_COURSES = [
    Course(
        course_code="TDT4140",
        name="Software Engineering",
        description="A course on software engineering principles.",
        learning_outcomes="Be able to develop software in a team.",
        exam_format="Digital exam",
        mandatory_assignments="3 assignments",
    ),
    Course(
        course_code="LOG200",
        name="Logistics Management",
        description="A course on logistics.",
        learning_outcomes="Understand supply chains.",
        exam_format="Written exam",
        mandatory_assignments="1 case study",
    ),
]


def test_retrieve_knowledge_success():
    """
    Tests successful retrieval of exam format.
    """
    parsed_query = ParsedQuery(
        intent="get_exam_format",
        course_code="TDT4140",
    )
    result = retrieve_knowledge(parsed_query, SAMPLE_COURSES)
    assert result == "Digital exam"


def test_retrieve_knowledge_course_not_found():
    """
    Tests retrieval when the course code does not exist in the knowledge base.
    """
    parsed_query = ParsedQuery(
        intent="get_exam_format",
        course_code="XYZ999",
    )
    result = retrieve_knowledge(parsed_query, SAMPLE_COURSES)
    assert result is None


def test_retrieve_knowledge_intent_not_found():
    """
    Tests retrieval when the intent does not map to a known attribute.
    """
    # The ParsedQuery model will not allow an invalid intent,
    # so we test the retriever with a valid intent but an unknown attribute
    # by temporarily modifying the mapping.
    parsed_query = ParsedQuery(
        intent="get_exam_format", #a valid intent
        course_code="TDT4140",
    )
    # To simulate an unhandled intent, we can't create an invalid ParsedQuery.
    # Instead, we assume the query parser produces a valid intent that the
    # retriever doesn't know how to handle. We'll simulate this by setting
    # a valid intent on an otherwise valid query, and expect None.
    parsed_query.intent = "get_course_professor" # a non-supported intent
    result = retrieve_knowledge(parsed_query, SAMPLE_COURSES)
    assert result is None


def test_retrieve_knowledge_attribute_is_none():
    """
    Tests retrieval when the requested attribute exists but is None for the course.
    """
    courses_with_none = SAMPLE_COURSES + [
        Course(
            course_code="NEW101",
            name="New Course",
            description="A new course.",
            learning_outcomes=None, # This is None
            exam_format="Oral exam",
            mandatory_assignments="None",
        )
    ]
    parsed_query = ParsedQuery(
        intent="get_learning_outcomes",
        course_code="NEW101",
    )
    result = retrieve_knowledge(parsed_query, courses_with_none)
    # The new implementation returns a string representation of the attribute.
    # When the attribute is None, getattr returns None, and the function returns None.
    assert result is None


def test_retrieve_knowledge_case_insensitivity():
    """
    Tests that course code matching is case-insensitive.
    """
    parsed_query = ParsedQuery(
        intent="get_mandatory_assignments",
        course_code="log200", # Lowercase
    )
    result = retrieve_knowledge(parsed_query, SAMPLE_COURSES)
    assert result == "1 case study"

