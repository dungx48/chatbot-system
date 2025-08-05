import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from core.orchestrator.rag_service_v1 import RAGServiceV1_0
from core.orchestrator.rag_service_v1_1 import RAGServiceV1_1
from core.models.request.chat_request import ChatRequest
from core.models.response.chat_response import ChatResponse

chat_router = APIRouter()

chat_service_v1 = RAGServiceV1_0()
chat_service_v1_1 = RAGServiceV1_1()



@chat_router.post("/chat/v1", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, svc: RAGServiceV1_0 = Depends(lambda: chat_service_v1)):
    result = await svc.chat(req)
    return ChatResponse(**result)

@chat_router.post("/chat/v1_1")
async def chat_stream(req: ChatRequest, svc: RAGServiceV1_1 = Depends(lambda: chat_service_v1_1)):
    return StreamingResponse(
        svc.stream_chat(req),
        media_type="application/x-ndjson"
        )