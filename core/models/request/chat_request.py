from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_prompt: str
    question: str