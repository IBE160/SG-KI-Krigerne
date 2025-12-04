import json
from pathlib import Path
import pytest
import os # Import os for chmod check

from backend.src.db.knowledge_base_manager import (
    KNOWLEDGE_BASE_PATH, # Still need to import the default path if functions are called without path
    create_knowledge_base_if_not_exists,
    load_knowledge_base,
)
from backend.src.models.course import Course

@pytest.fixture(autouse=True)
def clean_test_environment(tmp_path):
    """Fixture to ensure the temporary test files and default KNOWLEDGE_BASE_PATH are cleaned before and after each test."""
    temp_kb_path = tmp_path / "temp_knowledge_base.json"
    
    # Clean temporary test file if it somehow exists
    if temp_kb_path.exists():
        temp_kb_path.unlink()
    
    # Clean the default KNOWLEDGE_BASE_PATH if it's created during tests that touch it
    if KNOWLEDGE_BASE_PATH.exists():
        KNOWLEDGE_BASE_PATH.unlink()
    
    yield
    
    # Post-test cleanup
    if temp_kb_path.exists():
        temp_kb_path.unlink()
    if KNOWLEDGE_BASE_PATH.exists():
        KNOWLEDGE_BASE_PATH.unlink()

def test_create_knowledge_base_if_not_exists_creates_file(tmp_path):
    """Test that the knowledge base file is created if it doesn't exist."""
    temp_kb_path = tmp_path / "temp_knowledge_base.json"
    create_knowledge_base_if_not_exists(temp_kb_path)
    assert temp_kb_path.exists()
    with open(temp_kb_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data == []


def test_create_knowledge_base_if_not_exists_does_not_overwrite(tmp_path):
    """Test that the knowledge base file is not overwritten if it already exists."""
    temp_kb_path = tmp_path / "temp_knowledge_base.json"
    # Create a dummy file with content
    existing_content = [{"course_code": "EXIST101", "name": "Existing Course", "learning_outcomes": "Existing data", "exam_format": "Oral", "mandatory_assignments": "None"}]
    with open(temp_kb_path, "w", encoding="utf-8") as f:
        json.dump(existing_content, f)

    create_knowledge_base_if_not_exists(temp_kb_path)
    assert temp_kb_path.exists()
    with open(temp_kb_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data == existing_content # Content should remain unchanged


def test_load_knowledge_base_loads_valid_json_and_parses_courses(tmp_path):
    """Test that a valid JSON file is loaded and parsed into Course objects."""
    temp_kb_path = tmp_path / "temp_knowledge_base.json"
    valid_data = [
        {"course_code": "TEST101", "name": "Test Course 1", "learning_outcomes": "LO1", "exam_format": "Exam", "mandatory_assignments": "Assignment1"},
        {"course_code": "TEST102", "name": "Test Course 2", "learning_outcomes": "LO2", "exam_format": "Project", "mandatory_assignments": "Assignment2"}
    ]
    with open(temp_kb_path, "w", encoding="utf-8") as f:
        json.dump(valid_data, f)
    
    courses = load_knowledge_base(temp_kb_path)
    assert len(courses) == 2
    assert all(isinstance(course, Course) for course in courses)
    assert courses[0].course_code == "TEST101"
    assert courses[1].learning_outcomes == "LO2"


def test_load_knowledge_base_handles_missing_file(tmp_path):
    """Test that load_knowledge_base returns an empty list if file is missing."""
    temp_kb_path = tmp_path / "temp_knowledge_base.json"
    courses = load_knowledge_base(temp_kb_path)
    assert courses == []
    assert temp_kb_path.exists() # Should create an empty file if not exists

def test_load_knowledge_base_handles_invalid_json(tmp_path):
    """Test that load_knowledge_base returns an empty list for invalid JSON."""
    temp_kb_path = tmp_path / "temp_knowledge_base.json"
    with open(temp_kb_path, "w", encoding="utf-8") as f:
        f.write("this is not valid json")
    
    courses = load_knowledge_base(temp_kb_path)
    assert courses == []


def test_load_knowledge_base_retrieves_dummy_course_data():
    """Test retrieval of dummy course data, as set up in the main KNOWLEDGE_BASE_PATH."""
    # This test directly interacts with the default KNOWLEDGE_BASE_PATH
    # to ensure the main application knowledge base handling is correct.
    # It assumes the file might already exist or needs creation with dummy data.

    # Ensure the main knowledge_base.json exists and has the dummy data
    create_knowledge_base_if_not_exists(KNOWLEDGE_BASE_PATH)
    
    # Add a dummy course if the file was just created and is empty
    # This block essentially replicates the logic in the __main__ part of knowledge_base_manager.py
    # to ensure the dummy data is present for testing the default path.
    current_kb = load_knowledge_base(KNOWLEDGE_BASE_PATH)
    if not current_kb: # Only add if empty after initial creation/load
        dummy_course = Course(
            course_code="TDT4140",
            name="Software Engineering",
            learning_outcomes="The student has deep knowledge of software design principles and patterns...",
            exam_format="4-hour written digital exam",
            mandatory_assignments="3 out of 4 assignments must be approved."
        )
        with open(KNOWLEDGE_BASE_PATH, "w", encoding="utf-8") as f:
            json.dump([dummy_course.model_dump()], f, indent=2)
        current_kb = load_knowledge_base(KNOWLEDGE_BASE_PATH) # Reload after adding dummy

    courses = load_knowledge_base(KNOWLEDGE_BASE_PATH)
    assert any(course.course_code == "TDT4140" for course in courses)
    tdt4140 = next(c for c in courses if c.course_code == "TDT4140")
    assert tdt4140.learning_outcomes == "The student has deep knowledge of software design principles and patterns..."