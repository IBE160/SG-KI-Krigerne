from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
from src.rag.query_parser import parse_query
from src.rag.knowledge_base_retriever import retrieve_knowledge
from src.db.knowledge_base_manager import load_knowledge_base

router = APIRouter()

class Query(BaseModel):
    query: str

# Define the path to the knowledge base
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent / "db" / "knowledge_base.json"

@router.post("/chat")
async def chat_endpoint(query: Query):
    """
    Endpoint for natural language queries.
    """
    # Load the knowledge base
    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_PATH)

    # Parse the query
    parsed_query = parse_query(query.query)

    # Retrieve knowledge
    retrieved_info = retrieve_knowledge(parsed_query, knowledge_base)

    if retrieved_info:
        return {"answer": retrieved_info}
    else:
        return {"answer": "I'm sorry, I couldn't find the information for that."}