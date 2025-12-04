# backend/tests/test_feedback_api.py
import pytest
from fastapi.testclient import TestClient # Import TestClient
from main import app # Assuming main.py is in the root of the backend directory
from unittest.mock import AsyncMock, patch
from backend.src.models.feedback import FeedbackCreate

# Initialize the TestClient
client = TestClient(app)

# Remove @pytest.mark.asyncio as TestClient requests are synchronous

def test_submit_feedback_success():
    """
    Test successful submission of feedback to the /feedback endpoint.
    (AC 3.1.2: Test POST /feedback endpoint request validation, Mock FeedbackService)
    """
    with patch('backend.src.services.feedback_service.feedback_service.record_feedback', new_callable=AsyncMock) as mock_record_feedback:
        mock_record_feedback.return_value = {"message": "Feedback received successfully (mocked persistence)."}

        # Use the synchronous client for the test
        feedback_data = {
            "query": "What is MAT100 about?",
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 1
        }
        response = client.post("/feedback", json=feedback_data)

        assert response.status_code == 200
        assert response.json() == {"data": {"message": "Feedback received successfully (mocked persistence)."}}
        mock_record_feedback.assert_called_once_with(FeedbackCreate(**feedback_data))

def test_submit_feedback_invalid_rating():
    """
    Test feedback submission with an invalid rating.
    (AC 3.1.2: Test POST /feedback endpoint request validation)
    """
    with patch('backend.src.services.feedback_service.feedback_service.record_feedback', new_callable=AsyncMock) as mock_record_feedback:
        feedback_data = {
            "query": "What is MAT100 about?",
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 5 # Invalid rating
        }
        response = client.post("/feedback", json=feedback_data)

        assert response.status_code == 422 # Unprocessable Entity due to Pydantic validation
        assert "Input should be less than or equal to 1" in response.json()['detail'][0]['msg']
        mock_record_feedback.assert_not_called()

def test_submit_feedback_missing_field():
    """
    Test feedback submission with a missing required field.
    (AC 3.1.2: Test POST /feedback endpoint request validation)
    """
    with patch('backend.src.services.feedback_service.feedback_service.record_feedback', new_callable=AsyncMock) as mock_record_feedback:
        feedback_data = {
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 1
        }
        response = client.post("/feedback", json=feedback_data)

        assert response.status_code == 422 # Unprocessable Entity
        assert "Field required" in response.json()['detail'][0]['msg']
        mock_record_feedback.assert_not_called()

def test_submit_feedback_service_exception():
    """
    Test feedback submission when the FeedbackService raises an exception.
    """
    with patch('backend.src.services.feedback_service.feedback_service.record_feedback', new_callable=AsyncMock) as mock_record_feedback:
        mock_record_feedback.side_effect = Exception("Database connection failed")

        feedback_data = {
            "query": "What is MAT100 about?",
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 1
        }
        response = client.post("/feedback", json=feedback_data)

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error: Database connection failed"}
        mock_record_feedback.assert_called_once_with(FeedbackCreate(**feedback_data))
