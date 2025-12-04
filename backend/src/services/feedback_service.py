import logging
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.feedback import FeedbackCreate
from backend.src.db.feedback_repository import FeedbackRepository

logger = logging.getLogger(__name__)

class FeedbackService:
    def __init__(self, db: AsyncSession):
        self.feedback_repo = FeedbackRepository(db)

    async def record_feedback(self, feedback_data: FeedbackCreate):
        """
        Records user feedback by persisting it to the database.
        """
        try:
            feedback_record = await self.feedback_repo.create_feedback(feedback_data)
            logger.info(f"Feedback recorded successfully with ID: {feedback_record.id}, rating: {feedback_record.rating}")
            return {"message": "Feedback received successfully."}
        except Exception as e:
            logger.error(f"Error recording feedback: {e}", exc_info=True)
            raise # Re-raise the exception to be caught by the API handler