import json
from pathlib import Path
import pytest

from backend.src.db.knowledge_base_manager import (
    KNOWLEDGE_BASE_PATH, # Still need to import the default path if functions are called without path
    create_knowledge_base_if_not_exists,
    load_knowledge_base,
)
from backend.src.models.course import Course

# Define a temporary knowledge base path for testing
# This will be passed explicitly to the functions
TEMP_KNOWLEDGE_BASE_PATH = Path("backend/src/db/temp_knowledge_base.json")

@pytest.fixture(autouse=True)
def clean_temp_knowledge_base_file():
    """Fixture to ensure the temporary test file is cleaned before and after each test."""
    if TEMP_KNOWLEDGE_BASE_PATH.exists():
        TEMP_KNOWLEDGE_BASE_PATH.unlink()
    # Also clean the default KNOWLEDGE_BASE_PATH for the last test
    if KNOWLEDGE_BASE_PATH.exists():
        KNOWLEDGE_BASE_PATH.unlink()
    yield
    if TEMP_KNOWLEDGE_BASE_PATH.exists():
        TEMP_KNOWLEDGE_BASE_PATH.unlink()
    if KNOWLEDGE_BASE_PATH.exists():
        KNOWLEDGE_BASE_PATH.unlink()

def test_create_knowledge_base_if_not_exists_creates_file():
    """Test that the knowledge base file is created if it doesn't exist."""
    create_knowledge_base_if_not_exists(TEMP_KNOWLEDGE_BASE_PATH)
    assert TEMP_KNOWLEDGE_BASE_PATH.exists()
    with open(TEMP_KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data == []


def test_create_knowledge_base_if_not_exists_does_not_overwrite():
    """Test that the knowledge base file is not overwritten if it already exists."""
    # Create a dummy file with content
    existing_content = [{"course_code": "EXIST101", "learning_outcomes": "Existing data", "exam_format": "Oral", "mandatory_assignments": "None"}]
    with open(TEMP_KNOWLEDGE_BASE_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_content, f)

    create_knowledge_base_if_not_exists(TEMP_KNOWLEDGE_BASE_PATH)
    assert TEMP_KNOWLEDGE_BASE_PATH.exists()
    with open(TEMP_KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data == existing_content # Content should remain unchanged


def test_load_knowledge_base_loads_valid_json_and_parses_courses():
    """Test that a valid JSON file is loaded and parsed into Course objects."""
    valid_data = [
        {"course_code": "TEST101", "learning_outcomes": "LO1", "exam_format": "Exam", "mandatory_assignments": "Assignment1"},
        {"course_code": "TEST102", "learning_outcomes": "LO2", "exam_format": "Project", "mandatory_assignments": "Assignment2"}
    ]
    with open(TEMP_KNOWLEDGE_BASE_PATH, "w", encoding="utf-8") as f:
        json.dump(valid_data, f)
    
    courses = load_knowledge_base(TEMP_KNOWLEDGE_BASE_PATH)
    assert len(courses) == 2
    assert all(isinstance(course, Course) for course in courses)
    assert courses[0].course_code == "TEST101"
    assert courses[1].learning_outcomes == "LO2"


def test_load_knowledge_base_handles_missing_file():
    """Test that load_knowledge_base returns an empty list if file is missing."""
    courses = load_knowledge_base(TEMP_KNOWLEDGE_BASE_PATH)
    assert courses == []
    assert TEMP_KNOWLEDGE_BASE_PATH.exists() # Should create an empty file if not exists


def test_load_knowledge_base_handles_invalid_json():
    """Test that load_knowledge_base returns an empty list for invalid JSON."""
    with open(TEMP_KNOWLEDGE_BASE_PATH, "w", encoding="utf-8") as f:
        f.write("this is not valid json")
    
    courses = load_knowledge_base(TEMP_KNOWLEDGE_BASE_PATH)
    assert courses == []


def test_load_knowledge_base_retrieves_dummy_course_data():
    """Test retrieval of dummy course data, as set up in the main KNOWLEDGE_BASE_PATH."""
    # This test directly interacts with the default KNOWLEDGE_BASE_PATH
    # to ensure the main application knowledge base handling is correct.
    # It assumes the file might already exist or needs creation with dummy data.

    # Ensure the main knowledge_base.json exists and has the dummy data
    create_knowledge_base_if_not_exists(KNOWLEDGE_BASE_PATH)
    
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
        current_data = json.load(f)
    
    if not current_data or not any(c.get("course_code") == "TDT4140" for c in current_data):
        dummy_course_data = {
            "course_code": "TDT4140",
            "learning_outcomes": "The student has deep knowledge of software design principles and patterns...",
            "exam_format": "4-hour written digital exam",
            "mandatory_assignments": "3 out of 4 assignments must be approved."
        }
        if not current_data:
            current_data = [dummy_course_data]
        else:
            current_data.append(dummy_course_data)
        
        with open(KNOWLEDGE_BASE_PATH, "w", encoding="utf-8") as f:
            json.dump(current_data, f, indent=2)

    courses = load_knowledge_base(KNOWLEDGE_BASE_PATH)
    assert any(course.course_code == "TDT4140" for course in courses)
    tdt4140 = next(c for c in courses if c.course_code == "TDT4140")
    assert tdt4140.learning_outcomes == "The student has deep knowledge of software design principles and patterns..."