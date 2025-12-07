import pytest
from backend.src.rag.query_parser import parse_query, ParsedQuery

@pytest.mark.parametrize("query, expected", [
    ("what is the exam format for TDT4140?", ParsedQuery(intent="get_exam_format", course_code="TDT4140")),
    ("learning outcomes for MAT100", ParsedQuery(intent="get_learning_outcomes", course_code="MAT100")),
    ("mandatory assignments for LOG200", ParsedQuery(intent="get_mandatory_assignments", course_code="LOG200")),
    ("tell me about DAT220", ParsedQuery(intent=None, course_code="DAT220")),
    ("what is the exam format?", ParsedQuery(intent="get_exam_format", course_code=None)),
])
def test_parse_query(query, expected):
    """
    Test the parse_query function.
    """
    assert parse_query(query) == expected
