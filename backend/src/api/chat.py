from fastapi import APIRouter, Request
from pydantic import BaseModel
from src.rag.query_parser import parse_query
from src.rag.knowledge_base_retriever import retrieve_knowledge
from src.rag.generator import generate_response
from starlette.responses import StreamingResponse
import json
import asyncio

router = APIRouter()

class Query(BaseModel):
    query: str

async def event_generator(response_content: str):
    """Generates SSE compliant events."""
    # For MVP, send the entire response as one chunk
    chunk = {"type": "chunk", "content": response_content}
    yield f"data: {json.dumps(chunk)}\n\n"
    
    # Signal completion
    done_chunk = {"type": "done"}
    yield f"data: {json.dumps(done_chunk)}\n\n"

@router.post("/chat")
async def chat_endpoint(query: Query, request: Request):
    """
    Endpoint for natural language queries, streaming conversational responses via SSE.
    """
    # Access the pre-loaded knowledge base from the app state
    knowledge_base = request.app.state.knowledge_base

    # Parse the query
    parsed_query = parse_query(query.query)

    # Retrieve knowledge
    retrieved_info = retrieve_knowledge(parsed_query, knowledge_base)

    # Generate conversational response
    conversational_response = generate_response(parsed_query, retrieved_info)

    return StreamingResponse(event_generator(conversational_response), media_type="text/event-stream")