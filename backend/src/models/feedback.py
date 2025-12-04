# backend/src/models/feedback.py
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class FeedbackBase(BaseModel):
    query: str = Field(..., description="The user's original query.")
    response: str = Field(..., description="The chatbot's response that was rated.")
    rating: int = Field(..., description="User rating: 1 for thumbs up, -1 for thumbs down.", ge=-1, le=1)

class FeedbackCreate(FeedbackBase):
    # This model is used for incoming feedback data from the API
    pass

class FeedbackDB(FeedbackBase):
    id: UUID
    timestamp: datetime
    session_id: UUID | None = None

    class Config:
        from_attributes = True # Formerly orm_mode = True
