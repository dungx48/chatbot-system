from fastapi import FastAPI
from concurrent.futures.thread import ThreadPoolExecutor

from src.api.router import chat_router, chunking_router

app = FastAPI(title="Orchestrator Service")

app.include_router(chat_router)
app.include_router(chunking_router)