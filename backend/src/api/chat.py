from fastapi import APIRouter
from pydantic import BaseModel
from backend.src.rag.query_parser import parse_query

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(query: Query):
    """
    Endpoint for natural language queries.
    """
    parsed_query = parse_query(query.query)
    return parsed_query