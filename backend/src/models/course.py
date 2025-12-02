from pydantic import BaseModel

class Course(BaseModel):
    course_code: str
    learning_outcomes: str
    exam_format: str
    mandatory_assignments: str
