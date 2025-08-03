from pydantic import BaseModel
from typing import List


class ChatResponse(BaseModel):
    answer: str = ""
    think: str = ""
    process_times: dict = {}
    router_result: dict = {}
    source_docs: List[str] = []
    embedded_question: List[float] = None