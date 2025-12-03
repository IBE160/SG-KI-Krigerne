from fastapi import FastAPI
from src.api import chat

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

