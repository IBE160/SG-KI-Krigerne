import json
from pathlib import Path
from typing import List
import os

from backend.src.models.course import Course

KNOWLEDGE_BASE_PATH = Path("backend/src/db/knowledge_base.json")

def create_knowledge_base_if_not_exists(path: Path = KNOWLEDGE_BASE_PATH):
    """
    Creates an empty knowledge_base.json file if it does not already exist.
    """
    if not path.exists():
        initial_data = [] # Or include a dummy course if always present on creation
        try:
            path.parent.mkdir(parents=True, exist_ok=True) # Ensure parent directories exist
            with open(path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)
            print(f"Created empty knowledge base at: {path}")
            # Ensure proper file permissions: owner read/write, others read-only
            os.chmod(path, 0o644) 
        except IOError as e:
            print(f"Error creating knowledge base file: {e}")

def load_knowledge_base(path: Path = KNOWLEDGE_BASE_PATH) -> List[Course]:
    """
    Loads and parses the knowledge_base.json file.

    Args:
        path: The path to the knowledge base file.

    Returns:
        A list of Course objects.
    """
    create_knowledge_base_if_not_exists(path) # Ensure file exists before attempting to load
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        courses = [Course(**item) for item in data]
        return courses
    except FileNotFoundError:
        print(f"Knowledge base file not found at: {path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from knowledge base file: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading knowledge base: {e}")
        return []

if __name__ == "__main__":
    # Example usage:
    create_knowledge_base_if_not_exists()
    
    # Add a dummy course if the file was just created and is empty
    current_kb = load_knowledge_base()
    if not current_kb:
        dummy_course = Course(
            course_code="TDT4140",
            learning_outcomes="The student has deep knowledge of software design principles and patterns...",
            exam_format="4-hour written digital exam",
            mandatory_assignments="3 out of 4 assignments must be approved."
        )
        with open(KNOWLEDGE_BASE_PATH, "w", encoding="utf-8") as f:
            json.dump([dummy_course.dict()], f, indent=2)
        print("Added dummy course to knowledge base.")
        current_kb = load_knowledge_base() # Reload after adding dummy

    print("\nLoaded Knowledge Base:")
    for course in current_kb:
        print(course.json(indent=2))
