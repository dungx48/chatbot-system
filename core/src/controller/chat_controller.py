from fastapi import Depends

from core.src.api.router import chat_router
from core.src.services.chat_service import ChatService
from core.src.models.request import ChatRequest, ChatResponse

def get_service():
    embedding = EmbeddingAdapter()
    retrieval = RetrievalAdapter()
    inference = InferenceAdapter()
    return ChatService(embedding, retrieval, inference)

@chat_router.post("/chat")
async def chat_endpoint(req: ChatRequest, svc: ChatService = Depends(get_service)):
    return await svc.handle(req.question)
