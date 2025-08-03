from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_prompt: str = "Là một nhân viên ngân hàng, tôi sẽ tư vấn cho khách"
    question: str