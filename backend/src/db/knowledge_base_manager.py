import json
from typing import List
from pathlib import Path

from backend.src.models.course import Course


def load_knowledge_base() -> List[Course]:
    """
    Load courses from knowledge_base.json.

    Expected JSON format:

    {
      "courses": [
        {
          "course_code": "ADM120",
          "learning_outcomes": "...",
          "exam_format": "...",
          "mandatory_assignments": "..."
        },
        ...
      ]
    }
    """
    kb_path = Path(__file__).with_name("knowledge_base.json")

    if not kb_path.exists():
        print(f"Knowledge base file not found at {kb_path}, returning empty list.")
        return []

    try:
        with kb_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        raw_courses = data.get("courses", [])

        courses: List[Course] = []

        # Handle both list-of-dicts and dict-of-dicts just in case
        if isinstance(raw_courses, list):
            for entry in raw_courses:
                if not isinstance(entry, dict):
                    print(f"Skipping non-dict entry in KB: {entry!r}")
                    continue
                courses.append(Course(**entry))
        elif isinstance(raw_courses, dict):
            for code, info in raw_courses.items():
                if not isinstance(info, dict):
                    print(f"Skipping non-dict entry for {code}: {info!r}")
                    continue
                payload = dict(info)
                payload.setdefault("course_code", code)
                courses.append(Course(**payload))
        else:
            print(f"Unexpected 'courses' type in KB: {type(raw_courses)}")

        print(f"Loaded {len(courses)} courses from knowledge base.")
        return courses

    except Exception as e:
        print(f"An unexpected error occurred while loading knowledge base: {e}")
        return []
