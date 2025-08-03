from pydantic import BaseModel

class GenerateAnswerResponse(BaseModel):
    think: str
    answer: str