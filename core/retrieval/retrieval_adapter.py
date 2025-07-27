from qdrant_client import QdrantClient
from core.common.config import settings

class RetrievalAdapter:
    def __init__(self):
        self.qdrant_collection_name = settings.QDRANT_COLLECTION_NAME
        self.qdrant_url = settings.QDRANT_URL
        self.vector_db = QdrantClient(url=self.qdrant_url)

    def get_retrieval(self, query_vector: list[float]) -> dict:
        results = self.vector_db.search(query_vector=query_vector,
                                        collection_name=self.qdrant_collection_name)
        return results