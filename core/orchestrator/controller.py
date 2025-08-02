from fastapi import APIRouter, Depends
from core.orchestrator.service import RAGService
from core.models.request.chat_request import ChatRequest
from core.models.response.chat_response import ChatResponse

chat_router = APIRouter()

chat_service = RAGService()


@chat_router.post("/chat/v1", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, svc: RAGService = Depends(lambda: chat_service)):
    result = await svc.chat(req)
    return ChatResponse(**result)