from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI, OpenAIError

from backend.src.rag.query_parser import ParsedQuery

# ---- LLM client helpers ----------------------------------------------------


_client: Optional[OpenAI] = None


def get_client() -> Optional[OpenAI]:
    """
    Lazily create an OpenAI client if an API key is configured.

    Returns None if OPENAI_API_KEY is not set so the app can still run
    without an LLM (it will just use a simple fallback answer).
    """
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # No key configured -> run in "non-LLM fallback" mode
        return None

    _client = OpenAI(api_key=api_key)
    return _client


# ---- Prompt construction ----------------------------------------------------


SYSTEM_PROMPT = """You are Himolde Study Friend, a helpful assistant for HiMolde students.

You answer questions about HiMolde courses based on the *Course info* that is
provided to you. If the supplied course info does not contain the answer, say
that you do not know and suggest checking the official course page.

Guidelines:
- Be friendly and concise.
- Focus on what the student actually asked for (exam format, learning outcomes,
  mandatory assignments, etc.).
- Where helpful, give 1–3 short study tips, but do not invent details that are
  not in the Course info.
"""


def _extract_user_query(parsed_query: ParsedQuery) -> str:
    """
    Best-effort way to get the original text the user typed from ParsedQuery,
    without depending too hard on its internal structure.
    """
    for attr in ("original_query", "raw_query", "query", "text"):
        if hasattr(parsed_query, attr):
            value = getattr(parsed_query, attr)
            if isinstance(value, str):
                return value

    # Fallback – not ideal, but at least something printable
    return str(parsed_query)


def _build_messages(
    parsed_query: ParsedQuery,
    retrieved_info: Optional[str],
    history: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    """
    Build the messages list for the Chat Completions API.
    """
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    # Add recent conversation history (last few turns is enough)
    if history:
        for msg in history[-6:]:
            role = msg.get("role")
            content = msg.get("content")
            if role in {"user", "assistant"} and isinstance(content, str):
                messages.append({"role": role, "content": content})

    # Provide the course information we retrieved (if any)
    if retrieved_info:
        messages.append(
            {
                "role": "system",
                "content": f"Course info (from the knowledge base):\n{retrieved_info}",
            }
        )
    else:
        messages.append(
            {
                "role": "system",
                "content": (
                    "No specific course info was found for this question. "
                    "If the user asks for something like exam format or "
                    "learning outcomes, you probably have to answer that "
                    "you don't know and suggest checking the official course page."
                ),
            }
        )

    # Current user question
    user_text = _extract_user_query(parsed_query)
    messages.append({"role": "user", "content": user_text})

    return messages


# ---- Public API -------------------------------------------------------------


def generate_response(
    parsed_query: ParsedQuery,
    retrieved_info: Optional[str],
    history: Optional[List[Dict[str, str]]] = None,
) -> str:
    """
    Generate a conversational response.

    If an OpenAI API key is configured, this uses the Chat Completions API.
    Otherwise it falls back to a simple, template-based answer.
    """
    client = get_client()

    # If no LLM configured, keep your old style of answer so the app still works.
    if client is None:
        if retrieved_info:
            return (
                "Here is what I found in the course information:\n\n"
                f"{retrieved_info}\n\n"
                "If you need more details, you may want to check the official "
                "course page."
            )
        else:
            return (
                "I couldn't find detailed information for that course in my "
                "knowledge base. You may want to check the official course page."
            )

    messages = _build_messages(parsed_query, retrieved_info, history or [])

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.4,
            max_completion_tokens=400,
        )
        content = completion.choices[0].message.content
        return content.strip() if content else "Sorry, I couldn't generate a response."
    except OpenAIError as e:
        # Log to console and fall back gracefully
        print(f"[generator] OpenAIError: {e}")  # you can swap this for proper logging

        if retrieved_info:
            return (
                "There was a problem talking to the language model.\n\n"
                "Here is the raw course info I have:\n\n"
                f"{retrieved_info}"
            )
        else:
            return (
                "There was a problem talking to the language model, and I also "
                "couldn't find this course in my knowledge base. "
                "Please try again or check the official course page."
            )
