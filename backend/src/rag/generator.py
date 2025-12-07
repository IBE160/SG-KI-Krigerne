from __future__ import annotations
import os
import logging
from typing import List, Dict, Any, Optional
import json

# *** IMPORTANT CHANGE 1: New Import ***
# We use 'from google import genai' instead of 'google.generativeai'
from google import genai 

from backend.src.rag.query_parser import ParsedQuery

# ----------------------------------------------------------------------
# Gemini Configuration (Updated for New SDK)
# ----------------------------------------------------------------------

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "No Gemini API key found. Set GEMINI_API_KEY (or GOOGLE_API_KEY) "
        "in your environment."
    )

# *** IMPORTANT CHANGE 2: Client Initialization ***
# 1. DELETE the old 'genai.configure(api_key=...)' call.
# 2. Create the client object here, passing the API key directly.
client = genai.Client(api_key=GEMINI_API_KEY) 

# Recommended High-RPD Model: Gemma 3-2b Instruction-Tuned (14.4K RPD)
MODEL_NAME = "gemini-2.5-flash-lite" 

SYSTEM_PROMPT = """
You are HiMolde Study Friend, a friendly chatbot that helps students at
Molde University College (HiMolde) understand their courses.

Rules:
- Only answer questions related to HiMolde courses, learning outcomes,
  exam formats, and mandatory assignments.
- When you are given structured course information, use it as the source
  of truth. Do NOT invent facts that are not in the course info.
- If the user asks about a course that does not exist in the knowledge
  base, say you cannot find it and suggest checking the official course
  pages.
- Keep answers concise, clear, and student-friendly.
- You may reference previous turns in the conversation to keep context.
"""

# ----------------------------------------------------------------------
# Helper functions (Kept exactly as in your original code)
# ----------------------------------------------------------------------

def _extract_user_query(parsed_query: ParsedQuery) -> str:
    """
    Try to recover the raw user question from ParsedQuery.
    """
    # We don't know exactly which attribute name you used in ParsedQuery,
    # so we try a few common ones and fall back to an empty string.
    """
    """
    for attr in ("original_query", "raw_query", "text", "query", "prompt"):
        if hasattr(parsed_query, attr):
            value = getattr(parsed_query, attr)
            if isinstance(value, str):
                return value
    return ""

def format_history(history: List[Dict[str, str]]) -> str:
    """
    Turn your stored history (list of {'role', 'content'}) into a simple
    text block for the model. We keep only the last few turns so it
    doesn't get too long.
    """
    if not history:
        return "No previous conversation."

    lines = []
    # keep the last 6 turns at most
    for message in history[-6:]:
        role = message.get("role", "user")
        content = message.get("content", "")
        prefix = "Student" if role == "user" else "Assistant"
        lines.append(f"{prefix}: {content}")
    return "\n".join(lines)

def _format_course_context(
    parsed_query: ParsedQuery,
    retrieved_info: Optional[Any],
) -> str:
    """
    Turn whatever 'retrieve_knowledge' returned into plain text.

    This function MUST always return a string—never a dict—otherwise
    join() will crash with `expected str instance, dict found`.
    """
    # Nothing found
    if retrieved_info is None:
        return ""

    # If the retriever returns a dict like
    # {"course_code": "ADM120", "name": "LEARNING",
    # "field": "exam format", "value": "..."}
    if isinstance(retrieved_info, dict):
        code = retrieved_info.get("course_code") or parsed_query.course_code or "Unknown course"
        name = retrieved_info.get("name") or ""
        field = retrieved_info.get("field")
        value = retrieved_info.get("value")

        lines = []

        # First line: course name
        course_line = f"Course: {code} {name}".strip()
        lines.append(course_line)

        # Second line: specific field/value if we have them
        if field and value:
            pretty_field = field.replace("_", " ").title()
            lines.append(f"{pretty_field}: {value}")
        else:
            # Fallback - dump the dict as JSON so we still give Gemini something usable
            lines.append(json.dumps(retrieved_info, ensure_ascii=False))
        
        return "\n".join(lines)

    # If it's already a string (or something string-like)
    return str(retrieved_info)

# ----------------------------------------------------------------------
# Public API used by chat.py
# ----------------------------------------------------------------------

def generate_response(
    parsed_query: Any,
    retrieved_info: Optional[str],
    history: List[Dict[str, str]],
) -> str:
    """
    Generate a conversational answer using Gemini.

    - parsed_query: output from query_parser.parse_query(...)
    - retrieved_info: string from retrieve_knowledge(...) (may be None)
    - history: list of messages like {"role": "user"|"assistant", "content": "..."}
    """
    user_question = _extract_user_query(parsed_query)
    conversation_block = format_history(history)
    course_block = _format_course_context(parsed_query, retrieved_info)

    # This is the single prompt we send to Gemini.
    prompt = f"""
You are HiMolde Study Friend.

System instructions:
{SYSTEM_PROMPT}

Conversation so far:
{conversation_block}

New student question:
{user_question}

Structured course information (if any):
{course_block}

Task:
Using ONLY the information above, answer the student's question in a
helpful, concise way. If the course information is missing or incomplete,
explain that clearly and suggest checking the official HiMolde course
pages.
"""

    try:
        # *** IMPORTANT CHANGE 3: The Call Method ***
        # We now call 'generate_content' on the client's 'models' service
        response = client.models.generate_content(
            model=MODEL_NAME, # Uses the high-RPD model defined globally
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                # system_instruction is now part of the contents/prompt template
                temperature=0.2,
                max_output_tokens=512,
            )
        )

        # google-generativeai exposes the main text via .text
        answer = (response.text or "").strip()
        if not answer:
            raise ValueError("Empty response from Gemini model")
        return answer
    
    except Exception as e:
        # Log the technical error, but return a student-friendly message.
        logger.error(f"Error calling Gemini model: {e}")

        if retrieved_info:
            # We still have something useful from the knowledge base
            return (
                "I couldn't reach the language model right now, but here's the "
                "information I have from the course database:\n\n"
                f"{retrieved_info}"
            )
        else:
            return (
                "I couldn't reach the language model and I also couldn't find "
                "this course in my local database. Please double-check the "
                "course code or check the official HiMolde course pages."
            )