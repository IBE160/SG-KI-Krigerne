from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.feedback import FeedbackCreate
from backend.src.services.feedback_service import FeedbackService # Import the class directly
from backend.src.db.database import get_db # Import the dependency

router = APIRouter()

@router.post("/feedback")
async def submit_feedback(
    feedback: FeedbackCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Allows users to submit feedback on chatbot responses.
    """
    try:
        feedback_service = FeedbackService(db) # Instantiate FeedbackService with the session
        response = await feedback_service.record_feedback(feedback)
        return {"data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")