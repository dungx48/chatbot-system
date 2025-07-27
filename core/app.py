from fastapi import FastAPI
from core.orchestrator.controller import chat_router

app = FastAPI(title="Chatbot System")
app.include_router(chat_router, prefix="/v1")