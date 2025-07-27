from core.common.calcu_process_time import measure_time
from .embedding_adapter import get_adapter

class EmbeddingService:
    def __init__(self, adapter_type: str, model_name: str = None):
        self.adapter = get_adapter(adapter_type, model_name)

    @measure_time
    def encode(self, doc: str) -> list[float]:
        embedding = self.adapter.get_embedding(doc)
        return embedding
