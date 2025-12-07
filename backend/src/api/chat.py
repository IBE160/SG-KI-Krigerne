from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Literal

from backend.src.rag.query_parser import parse_query
from backend.src.rag.knowledge_base_retriever import retrieve_knowledge
from backend.src.rag.generator import generate_response
from starlette.responses import StreamingResponse
import json
import asyncio

router = APIRouter()


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    query: str
    history: List[ChatMessage] = []


async def event_generator(response_content: str):
    chunk = {"type": "chunk", "content": response_content}
    yield f"data: {json.dumps(chunk)}\n\n"
    done = {"type": "done"}
    yield f"data: {json.dumps(done)}\n\n"


@router.post("/chat")
async def chat_endpoint(payload: ChatRequest, request: Request):
    knowledge_base = request.app.state.knowledge_base

    parsed_query = parse_query(payload.query, payload.history)
    retrieved_info = retrieve_knowledge(parsed_query, knowledge_base)

    conversational_response = generate_response(
        parsed_query,
        retrieved_info,
        [m.model_dump() for m in payload.history],
    )

    return StreamingResponse(
        event_generator(conversational_response),
        media_type="text/event-stream",
    )
