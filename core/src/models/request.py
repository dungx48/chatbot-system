from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[List[str]] = None

class DocumentRequest(BaseModel):
    document_id: str
    user_id: str

class EmbeddingRequest(BaseModel):
    text: str
    model: Optional[str] = "default-model"  # Specify a default model if needed

class RetrievalRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5  # Default to retrieving top 5 results
