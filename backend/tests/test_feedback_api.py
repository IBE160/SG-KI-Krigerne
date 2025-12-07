import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from unittest.mock import MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.src.models.feedback import FeedbackCreate, Feedback
from backend.src.db.database import get_db
from backend.main import app as real_app


# Test functions now explicitly use the client_with_test_db fixture
# and db_session_fixture where direct database interaction is needed.

@pytest.mark.asyncio
async def test_submit_feedback_success(test_app: TestClient):
    """
    Test that record_feedback successfully calls the service and returns a success message.
    Mocks the service layer to isolate API behavior.
    """
    with patch('backend.src.services.feedback_service.FeedbackService.record_feedback', new_callable=MagicMock) as mock_record_feedback:
        mock_record_feedback.return_value = {"message": "Feedback received successfully (mocked persistence)."}

        feedback_data = {
            "query": "What is MAT100 about?",
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 1
        }
        response = test_app.post("/feedback", json=feedback_data)

        assert response.status_code == 200
        assert response.json() == {"data": {"message": "Feedback received successfully (mocked persistence)."}}
        mock_record_feedback.assert_called_once()
        args, kwargs = mock_record_feedback.call_args
        called_feedback_create = args[0]
        assert isinstance(called_feedback_create, FeedbackCreate)
        assert called_feedback_create.query == feedback_data["query"]
        assert called_feedback_create.response == feedback_data["response"]
        assert called_feedback_create.rating == feedback_data["rating"]


@pytest.mark.asyncio
async def test_submit_feedback_invalid_rating(test_app: TestClient):
    """
    Test API validation for invalid rating.
    """
    with patch('backend.src.services.feedback_service.FeedbackService.record_feedback', new_callable=MagicMock) as mock_record_feedback:
        feedback_data = {
            "query": "What is MAT100 about?",
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 5 # Invalid rating
        }
        response = test_app.post("/feedback", json=feedback_data)

        assert response.status_code == 422
        assert "ensure this value is less than or equal to 1" in response.json()['detail'][0]['msg']
        mock_record_feedback.assert_not_called()

@pytest.mark.asyncio
async def test_submit_feedback_missing_field(test_app: TestClient):
    """
    Test API validation for missing fields.
    """
    with patch('backend.src.services.feedback_service.FeedbackService.record_feedback', new_callable=MagicMock) as mock_record_feedback:
        feedback_data = {
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 1
        }
        response = test_app.post("/feedback", json=feedback_data)

        assert response.status_code == 422
        assert "field required" in response.json()['detail'][0]['msg']
        mock_record_feedback.assert_not_called()

@pytest.mark.asyncio
async def test_submit_feedback_service_exception(test_app: TestClient):
    """
    Test that API handles exceptions from the service layer.
    """
    with patch('backend.src.services.feedback_service.FeedbackService.record_feedback', new_callable=MagicMock) as mock_record_feedback:
        mock_record_feedback.side_effect = Exception("Database connection failed")

        feedback_data = {
            "query": "What is MAT100 about?",
            "response": "MAT100 is an introductory course to mathematics.",
            "rating": 1
        }
        response = test_app.post("/feedback", json=feedback_data)

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error: Database connection failed"}
        mock_record_feedback.assert_called_once()
        args, kwargs = mock_record_feedback.call_args
        called_feedback_create = args[0]
        assert isinstance(called_feedback_create, FeedbackCreate)
        assert called_feedback_create.query == feedback_data["query"]
        assert called_feedback_create.response == feedback_data["response"]
        assert called_feedback_create.rating == feedback_data["rating"]


@pytest.mark.asyncio
async def test_submit_feedback_persists_to_db(test_app: TestClient, db_session_fixture: AsyncSession):
    """
    Test that feedback submitted via the API is correctly persisted to the database.
    (AC 3.2.1, AC 3.2.2)
    This is a true integration test, not mocking the persistence layer.
    """
    feedback_data = {
        "query": "Is there a final exam for history?",
        "response": "Yes, there is a final written exam for history.",
        "rating": -1
    }
    response = test_app.post("/feedback", json=feedback_data)

    assert response.status_code == 200
    assert response.json()["data"]["message"] == "Feedback received successfully."

    # Verify persistence by querying the database directly
    # Need to import Feedback model and select it from the db_session
    async with db_session_fixture.begin(): # Start a new transaction for querying
        stmt = select(Feedback).filter_by(query=feedback_data["query"], response=feedback_data["response"], rating=feedback_data["rating"])
        result = await db_session_fixture.execute(stmt)
        persisted_feedback = result.scalar_one_or_none()

    assert persisted_feedback is not None
    assert persisted_feedback.query == feedback_data["query"]
    assert persisted_feedback.response == feedback_data["response"]
    assert persisted_feedback.rating == feedback_data["rating"]


@pytest.mark.asyncio
async def test_get_db_override(test_app: TestClient, db_session_fixture: AsyncSession):
    """
    Test to explicitly verify that the get_db dependency is correctly overridden
    and yields an AsyncSession instance.
    """
    # This endpoint is just for testing the dependency override
    @test_app.app.get("/test-db-override")
    async def test_endpoint(db: AsyncSession = Depends(get_db)):
        # We can't directly assert on the object itself due to FastAPI's internal handling
        # but we can check its type or a unique attribute if available
        # Or even better, pass the original fixture into the app context for comparison
        return {"db_type": str(type(db)), "is_async_session": isinstance(db, AsyncSession)}

    response = test_app.get("/test-db-override")
    assert response.status_code == 200
    assert response.json()["is_async_session"] is True
    # We can't compare the actual objects directly as FastAPI yields them.
    # But checking the type and isinstance should be sufficient.
    assert "sqlalchemy.ext.asyncio.session.AsyncSession" in response.json()["db_type"]