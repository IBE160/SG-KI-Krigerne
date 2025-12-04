from src.rag.generator import generate_response
from src.rag.query_parser import ParsedQuery
import pytest

@pytest.fixture
def sample_parsed_query():
    """Fixture for a sample ParsedQuery."""
    return ParsedQuery(
        intent="get_exam_format",
        course_code="TDT4140",
        entities={"course_code": "TDT4140", "information_type": "exam_format"}
    )

@pytest.fixture
def sample_parsed_query_learning_outcomes():
    """Fixture for a sample ParsedQuery for learning outcomes."""
    return ParsedQuery(
        intent="get_learning_outcomes",
        course_code="TDT4140",
        entities={"course_code": "TDT4140", "information_type": "learning_outcomes"}
    )

@pytest.fixture
def sample_parsed_query_mandatory_assignments():
    """Fixture for a sample ParsedQuery for mandatory assignments."""
    return ParsedQuery(
        intent="get_mandatory_assignments",
        course_code="TDT4140",
        entities={"course_code": "TDT4140", "information_type": "mandatory_assignments"}
    )

@pytest.fixture
def sample_parsed_query_no_course():
    """Fixture for a ParsedQuery without a course code."""
    return ParsedQuery(
        intent="get_exam_format",
        course_code=None,
        entities={"information_type": "exam_format"}
    )

def test_generate_response_exam_format_found(sample_parsed_query):
    """Tests generating a response when exam format information is found."""
    retrieved_info = "4-hour written exam"
    expected_response = "The exam format for TDT4140 is: 4-hour written exam"
    actual_response = generate_response(sample_parsed_query, retrieved_info)
    assert actual_response == expected_response

def test_generate_response_learning_outcomes_found(sample_parsed_query_learning_outcomes):
    """Tests generating a response when learning outcomes information is found."""
    retrieved_info = "Understand algorithms, data structures, and software design principles"
    expected_response = "The learning outcomes for TDT4140 are: Understand algorithms, data structures, and software design principles"
    actual_response = generate_response(sample_parsed_query_learning_outcomes, retrieved_info)
    assert actual_response == expected_response

def test_generate_response_mandatory_assignments_found(sample_parsed_query_mandatory_assignments):
    """Tests generating a response when mandatory assignments information is found."""
    retrieved_info = "3 mandatory programming assignments"
    expected_response = "The mandatory assignments for TDT4140 are: 3 mandatory programming assignments"
    actual_response = generate_response(sample_parsed_query_mandatory_assignments, retrieved_info)
    assert actual_response == expected_response

def test_generate_response_info_not_found(sample_parsed_query):
    """Tests generating a response when information is not found (retrieved_info is None)."""
    retrieved_info = None
    expected_response = "I'm sorry, I couldn't find the information for that course. You may want to check the official course page."
    actual_response = generate_response(sample_parsed_query, retrieved_info)
    assert actual_response == expected_response

def test_generate_response_no_course_code_info_not_found(sample_parsed_query_no_course):
    """Tests generating a response when no course code and info is not found."""
    retrieved_info = None
    expected_response = "I'm sorry, I couldn't find the information for that course. You may want to check the official course page."
    actual_response = generate_response(sample_parsed_query_no_course, retrieved_info)
    assert actual_response == expected_response


