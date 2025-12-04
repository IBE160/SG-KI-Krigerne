from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.feedback import Feedback, FeedbackCreate

class FeedbackRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_feedback(self, feedback_data: FeedbackCreate) -> Feedback:
        db_feedback = Feedback(**feedback_data.dict())
        self.db.add(db_feedback)
        await self.db.commit()
        await self.db.refresh(db_feedback)
        return db_feedback
