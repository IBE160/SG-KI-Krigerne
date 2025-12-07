from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from backend.src.db.knowledge_base_manager import load_knowledge_base
from backend.src.api import chat, feedback
from backend.src.db.database import init_db_connection, get_engine, get_session_local # get_engine is still useful for disposing

# Define the path to the knowledge base
KNOWLEDGE_BASE_PATH = Path(__file__).parent / "src" / "db" / "knowledge_base.json"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB connection is now lazy-initialized via get_db dependency
    print("Application startup...")
    # Optionally force initialization if needed, but get_db/get_session_local will handle it
    # init_db_connection()

    # Load the knowledge base at startup
    print("Loading knowledge base...")
    knowledge_base = load_knowledge_base()
    app.state.knowledge_base = knowledge_base
    print("Knowledge base loaded.")
    yield
    # Clean up resources if needed on shutdown
    print("Shutting down...")
    # Dispose of the engine if it was initialized
    try:
        engine = get_engine()
        if engine:
            await engine.dispose()
    except RuntimeError:
        pass # Engine was never initialized, no need to dispose


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router)
app.include_router(feedback.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}