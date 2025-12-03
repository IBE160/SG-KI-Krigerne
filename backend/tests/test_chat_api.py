from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_chat_endpoint():
    """
    Test the /chat endpoint.
    """
    response = client.post("/chat", json={"query": "what is the exam format for TDT4140?"})
    assert response.status_code == 200
    assert response.json() == {
        "intent": "get_exam_format",
        "course_code": "TDT4140"
    }
