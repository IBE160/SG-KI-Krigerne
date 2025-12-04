from pydantic import BaseModel, Field
from uuid import UUID as PyUUID, uuid4 # Import uuid4
from datetime import datetime, timezone # Import timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # Keep for explicit PG type if needed
from sqlalchemy.sql import func
from sqlalchemy import Uuid # Import Uuid from sqlalchemy
import sqlalchemy as sa # Import sqlalchemy as sa for sa.text

from backend.src.db.database import Base # Import Base from your database setup
print(f"ID of Base in model (feedback.py): {id(Base)}") # Debug print

class FeedbackBase(BaseModel):
    query: str = Field(..., description="The user's original query.")
    response: str = Field(..., description="The chatbot's response that was rated.")
    rating: int = Field(..., description="User rating: 1 for thumbs up, -1 for thumbs down.", ge=-1, le=1)

class FeedbackCreate(FeedbackBase):
    # This model is used for incoming feedback data from the API
    pass

class FeedbackDB(FeedbackBase):
    id: PyUUID # Use PyUUID here
    timestamp: datetime
    session_id: PyUUID | None = None

    class Config:
        orm_mode = True # Use orm_mode for Pydantic v1 compatibility

# SQLAlchemy ORM model for the 'feedback' table
class Feedback(Base):
    __tablename__ = "feedback"

    # Use Uuid for generic UUID type and add Python-side default
    id = Column(Uuid, primary_key=True, default=uuid4)
    query = Column(String, nullable=False)
    response = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    # Use DateTime with timezone=True and add Python-side default
    timestamp = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    session_id = Column(Uuid, nullable=True) # Optional, for future session context
