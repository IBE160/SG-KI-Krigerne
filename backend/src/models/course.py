from pydantic import BaseModel
from typing import Optional

class Course(BaseModel):
    course_code: str
    name: str  # Add name field
    description: Optional[str] = None
    learning_outcomes: Optional[str] = None
    exam_format: Optional[str] = None
    mandatory_assignments: Optional[str] = None
