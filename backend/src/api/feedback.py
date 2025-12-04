# backend/src/api/feedback.py
from fastapi import APIRouter, HTTPException
from backend.src.models.feedback import FeedbackCreate
from backend.src.services.feedback_service import feedback_service

router = APIRouter()

@router.post("/feedback")
async def submit_feedback(feedback: FeedbackCreate):
    """
    Allows users to submit feedback on chatbot responses.
    """
    try:
        response = await feedback_service.record_feedback(feedback)
        return {"data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
