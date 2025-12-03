import pytest
from fastapi.testclient import TestClient
from main import app  # Corrected import
from src.models.course import Course

client = TestClient(app)

SAMPLE_COURSES = [
    Course(
        course_code="TDT4140",
        name="Software Engineering",
        learning_outcomes="Be able to develop software in a team.",
        exam_format="Digital exam",
        mandatory_assignments="3 assignments",
    )
]

def test_chat_endpoint_success(mocker):
    """
    Test the /chat endpoint for a successful retrieval.
    """
    # Mock the load_knowledge_base function
    mocker.patch(
        "src.api.chat.load_knowledge_base",
        return_value=SAMPLE_COURSES,
    )

    response = client.post("/chat", json={"query": "what is the exam format for TDT4140?"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Digital exam"}


def test_chat_endpoint_not_found(mocker):
    """
    Test the /chat endpoint when the course is not found.
    """
    # Mock the load_knowledge_base function
    mocker.patch(
        "src.api.chat.load_knowledge_base",
        return_value=SAMPLE_COURSES,
    )

    response = client.post("/chat", json={"query": "what is the exam format for XYZ999?"})
    assert response.status_code == 200
    assert response.json() == {"answer": "I'm sorry, I couldn't find the information for that."}
