from fastapi import APIRouter

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chunking_router = APIRouter(
    prefix="/chunking",
    tags=["Chunking"],
)