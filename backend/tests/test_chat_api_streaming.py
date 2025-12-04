from fastapi.testclient import TestClient
from main import app  # Assuming your main FastAPI app instance is in main.py
import pytest
import json
from unittest.mock import patch, MagicMock

# Create a TestClient for your FastAPI application
client = TestClient(app)

# Mock constants or dependencies if needed globally for these tests
MOCK_KNOWLEDGE_BASE_PATH = "mock/path/to/knowledge_base.json"

@pytest.fixture
def mock_dependencies():
    """
    Fixture to mock the dependencies for the chat endpoint.
    """
    with patch("src.api.chat.parse_query") as mock_parse_query, \
         patch("src.api.chat.retrieve_knowledge") as mock_retrieve_knowledge, \
         patch("src.api.chat.generate_response") as mock_generate_response:
        
        # Configure mocks
        # Mock knowledge_base object to be accessed by chat_endpoint
        client.app.state.knowledge_base = MagicMock()
        
        mock_parsed_query = MagicMock()
        mock_parsed_query.course_code = "TDT4140"
        mock_parsed_query.intent = "get_exam_format"
        mock_parse_query.return_value = mock_parsed_query

        mock_retrieve_knowledge.return_value = "4-hour written exam"
        mock_generate_response.return_value = "The exam format for TDT4140 is: 4-hour written exam"
        
        yield {
            "parse_query": mock_parse_query,
            "retrieve_knowledge": mock_retrieve_knowledge,
            "generate_response": mock_generate_response,
        }

def test_chat_endpoint_streaming_success(mock_dependencies):
    """
    Test that the /chat endpoint streams a successful conversational response.
    """
    response = client.post(
        "/chat",
        json={"query": "What is the exam format for TDT4140?"},
        headers={"Accept": "text/event-stream"}
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    received_chunks = []
    for line in response.iter_lines():
        if line.startswith("data: "):
            json_str = line[len("data: "):].strip()
            received_chunks.append(json.loads(json_str))
    
    # Verify the chunk format and content
    assert len(received_chunks) == 2
    assert received_chunks[0]["type"] == "chunk"
    assert received_chunks[0]["content"] == "The exam format for TDT4140 is: 4-hour written exam"
    assert received_chunks[1]["type"] == "done"

    # Verify dependencies were called
    mock_dependencies["parse_query"].assert_called_once()
    mock_dependencies["retrieve_knowledge"].assert_called_once()
    mock_dependencies["generate_response"].assert_called_once()


def test_chat_endpoint_streaming_no_info_found(mock_dependencies):
    """
    Test that the /chat endpoint streams an "information not found" response.
    """
    mock_dependencies["retrieve_knowledge"].return_value = None
    mock_dependencies["generate_response"].return_value = "I'm sorry, I couldn't find the information for that course. You may want to check the official course page."

    response = client.post(
        "/chat",
        json={"query": "What is the exam format for TDT4140?"},
        headers={"Accept": "text/event-stream"}
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    received_chunks = []
    for line in response.iter_lines():
        if line.startswith("data: "):
            json_str = line[len("data: "):].strip()
            received_chunks.append(json.loads(json_str))
    
    assert len(received_chunks) == 2
    assert received_chunks[0]["type"] == "chunk"
    assert received_chunks[0]["content"] == "I'm sorry, I couldn't find the information for that course. You may want to check the official course page."
    assert received_chunks[1]["type"] == "done"

    mock_dependencies["retrieve_knowledge"].assert_called_once()
    mock_dependencies["generate_response"].assert_called_once()

# TODO: Add a test for response time (AC 4) - this might require a different testing approach
