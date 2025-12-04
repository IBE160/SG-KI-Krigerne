# backend/src/services/feedback_service.py
from backend.src.models.feedback import FeedbackCreate

class FeedbackService:
    def __init__(self):
        # For Story 3.1, persistence is mocked.
        # In Story 3.2, this will be updated to interact with a repository.
        pass

    async def record_feedback(self, feedback_data: FeedbackCreate):
        """
        Records user feedback. For Story 3.1, this is a mock implementation.
        Actual persistence will be handled in Story 3.2.
        """
        print(f"MOCK: Recording feedback: {feedback_data.model_dump_json()}")
        # In Story 3.2, this will call a repository method to save to DB
        return {"message": "Feedback received successfully (mocked persistence)."}

feedback_service = FeedbackService()
