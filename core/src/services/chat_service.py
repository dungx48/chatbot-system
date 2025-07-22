from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

class ChatService:
    def __init__(self, cache_service, embedding_service, retrieval_service, inference_service):
        self.cache_service = cache_service
        self.embedding_service = embedding_service
        self.retrieval_service = retrieval_service
        self.inference_service = inference_service

    def process_chat(self, chat_request: ChatRequest) -> ChatResponse:
        # Validate input
        if not chat_request.user_id or not chat_request.message:
            raise HTTPException(status_code=400, detail="Invalid input data")

        # Generate embeddings
        embeddings = self.embedding_service.generate_embeddings(chat_request.message)

        # Retrieve relevant data
        relevant_data = self.retrieval_service.retrieve_data(embeddings)

        # Get inference result
        inference_result = self.inference_service.get_inference(relevant_data)

        # Create response
        response = ChatResponse(response=inference_result)
        return response