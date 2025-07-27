from core.common.calcu_process_time import measure_time
from .retrieval_adapter import RetrievalAdapter

class RetrievalService:
    def __init__(self):
        self.adapter = RetrievalAdapter()
    
    @measure_time
    def search(self, vector_question: list[float]) -> dict:
        return self.adapter.get_retrieval(query_vector=vector_question)
