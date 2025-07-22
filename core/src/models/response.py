from pydantic import BaseModel
from typing import List, Optional

class ChatResponse(BaseModel):
    message: str
    timestamp: str

class ChatHistoryResponse(BaseModel):
    history: List[ChatResponse]
    total_messages: int
    next_page_token: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    code: int
    details: Optional[str] = None