import pytest
import logging # Added import
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.services.feedback_service import FeedbackService, logger
from backend.src.models.feedback import FeedbackCreate, Feedback
from uuid import UUID, uuid4
from datetime import datetime

@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def feedback_service_instance(mock_db_session):
    return FeedbackService(mock_db_session)

@pytest.fixture
def sample_feedback_create():
    return FeedbackCreate(
        query="What is MAT100?",
        response="MAT100 is an introductory course.",
        rating=1
    )

@pytest.fixture
def sample_feedback_db(sample_feedback_create):
    return Feedback(
        id=uuid4(),
        timestamp=datetime.now(),
        **sample_feedback_create.dict()
    )

@pytest.mark.asyncio
async def test_record_feedback_success(feedback_service_instance, sample_feedback_create, sample_feedback_db):
    """
    Test that record_feedback successfully calls the repository and returns a success message.
    """
    with patch('backend.src.db.feedback_repository.FeedbackRepository.create_feedback', new_callable=AsyncMock) as mock_create_feedback:
        mock_create_feedback.return_value = sample_feedback_db
        response = await feedback_service_instance.record_feedback(sample_feedback_create)

        mock_create_feedback.assert_called_once_with(sample_feedback_create)
        assert response == {"message": "Feedback received successfully."}

@pytest.mark.asyncio
async def test_record_feedback_logs_success(feedback_service_instance, sample_feedback_create, sample_feedback_db, caplog):
    """
    Test that record_feedback logs a success message without sensitive data.
    """
    with patch('backend.src.db.feedback_repository.FeedbackRepository.create_feedback', new_callable=AsyncMock) as mock_create_feedback:
        mock_create_feedback.return_value = sample_feedback_db
        
        with caplog.at_level(logging.INFO): # Changed to logging.INFO
            await feedback_service_instance.record_feedback(sample_feedback_create)
            
            assert len(caplog.records) == 1
            record = caplog.records[0]
            assert record.levelname == 'INFO'
            assert f"Feedback recorded successfully with ID: {sample_feedback_db.id}, rating: {sample_feedback_db.rating}" in record.message
            assert "query" not in record.message
            assert "response" not in record.message

@pytest.mark.asyncio
async def test_record_feedback_handles_repository_exception(feedback_service_instance, sample_feedback_create):
    """
    Test that record_feedback propagates exceptions from the repository.
    """
    with patch('backend.src.db.feedback_repository.FeedbackRepository.create_feedback', new_callable=AsyncMock) as mock_create_feedback:
        mock_create_feedback.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await feedback_service_instance.record_feedback(sample_feedback_create)