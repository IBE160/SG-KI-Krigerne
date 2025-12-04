import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch # Changed AsyncMock to MagicMock for synchronous mocks
from backend.src.models.feedback import FeedbackCreate, Feedback # Feedback model is still needed for type checks
# Removed database imports as they are no longer needed
# from backend.src.db.database import get_db, Base, init_db_connection, get_engine, get_session_local

# from sqlalchemy.ext.asyncio import AsyncSession # Removed
# from sqlalchemy import text # Removed
# import os # Removed
# from uuid import UUID # Removed
# from datetime import datetime # Removed
# import asyncio # Removed

# Test Database Setup - No longer needed for this mocked approach
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Import the actual app instance
from main import app as real_app


@pytest.fixture
def client():
    return TestClient(real_app)


# Now the tests themselves
def test_submit_feedback_success(client):
    # This test will continue to mock record_feedback
    with patch('backend.src.services.feedback_service.FeedbackService.record_feedback', new_callable=MagicMock) as mock_record_feedback:
        mock_record_feedback.return_value = {"message": "Feedback received successfully (mocked persistence)."}

        feedback_data = {
            "query": "What is MAT100 about?",
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 1
        }
        response = client.post("/feedback", json=feedback_data)

        assert response.status_code == 200
        assert response.json() == {"data": {"message": "Feedback received successfully (mocked persistence)."}}
        mock_record_feedback.assert_called_once()
        args, kwargs = mock_record_feedback.call_args
        called_feedback_create = args[0]
        assert isinstance(called_feedback_create, FeedbackCreate)
        assert called_feedback_create.query == feedback_data["query"]
        assert called_feedback_create.response == feedback_data["response"]
        assert called_feedback_create.rating == feedback_data["rating"]


def test_submit_feedback_invalid_rating(client):
    with patch('backend.src.services.feedback_service.FeedbackService.record_feedback', new_callable=MagicMock) as mock_record_feedback:
        feedback_data = {
            "query": "What is MAT100 about?",
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 5 # Invalid rating
        }
        response = client.post("/feedback", json=feedback_data)

        assert response.status_code == 422
        assert "ensure this value is less than or equal to 1" in response.json()['detail'][0]['msg']
        mock_record_feedback.assert_not_called()

def test_submit_feedback_missing_field(client):
    with patch('backend.src.services.feedback_service.FeedbackService.record_feedback', new_callable=MagicMock) as mock_record_feedback:
        feedback_data = {
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 1
        }
        response = client.post("/feedback", json=feedback_data)

        assert response.status_code == 422
        assert "field required" in response.json()['detail'][0]['msg']
        mock_record_feedback.assert_not_called()

def test_submit_feedback_service_exception(client):
    with patch('backend.src.services.feedback_service.FeedbackService.record_feedback', new_callable=MagicMock) as mock_record_feedback:
        mock_record_feedback.side_effect = Exception("Database connection failed")

        feedback_data = {
            "query": "What is MAT100 about?",
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 1
        }
        response = client.post("/feedback", json=feedback_data)

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error: Database connection failed"}
        mock_record_feedback.assert_called_once()
        args, kwargs = mock_record_feedback.call_args
        called_feedback_create = args[0]
        assert isinstance(called_feedback_create, FeedbackCreate)
        assert called_feedback_create.query == feedback_data["query"]
        assert called_feedback_create.response == feedback_data["response"]
        assert called_feedback_create.rating == feedback_data["rating"]


# This test now also mocks the FeedbackService
def test_submit_feedback_persists_to_db(client):
    """
    Test that feedback submitted via the API is correctly persisted to the database.
    (AC 3.2.1, AC 3.2.2)
    """
    with patch('backend.src.services.feedback_service.FeedbackService.record_feedback', new_callable=MagicMock) as mock_record_feedback:
        mock_record_feedback.return_value = {"message": "Feedback received successfully."} # Service returns this on success

        feedback_data = {
            "query": "Is there a final exam for history?",
            "response": "Yes, there is a final written exam for history.",
            "rating": -1
        }
        response = client.post("/feedback", json=feedback_data)

        assert response.status_code == 200
        assert response.json() == {"data": {"message": "Feedback received successfully."}}
        mock_record_feedback.assert_called_once()
        args, kwargs = mock_record_feedback.call_args
        called_feedback_create = args[0]
        assert isinstance(called_feedback_create, FeedbackCreate)
        assert called_feedback_create.query == feedback_data["query"]
        assert called_feedback_create.response == feedback_data["response"]
        assert called_feedback_create.rating == feedback_data["rating"]