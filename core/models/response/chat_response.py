from pydantic import BaseModel
from typing import List


class ChatResponse(BaseModel):
    answer: str
    process_times: dict = {}
    source_docs: List[str] = []
    embedded_question: List[float] = None