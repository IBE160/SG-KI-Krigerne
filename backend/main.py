from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path
from src.db.knowledge_base_manager import load_knowledge_base
from src.api import chat, feedback

# Define the path to the knowledge base
KNOWLEDGE_BASE_PATH = Path(__file__).parent / "src" / "db" / "knowledge_base.json"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the knowledge base at startup
    print("Loading knowledge base...")
    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_PATH)
    app.state.knowledge_base = knowledge_base
    print("Knowledge base loaded.")
    yield
    # Clean up resources if needed on shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(chat.router)
app.include_router(feedback.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

