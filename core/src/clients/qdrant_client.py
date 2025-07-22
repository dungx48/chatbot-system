from qdrant_client import QdrantClient

class QdrantAdapter:
    def __init__(self, host: str, port: int):
        self.client = QdrantClient(host=host, port=port)

    def create_collection(self, collection_name: str, vector_size: int):
        self.client.recreate_collection(
            collection_name=collection_name,
            vector_size=vector_size,
            distance='Cosine'
        )

    def add_documents(self, collection_name: str, documents: list):
        self.client.upload_documents(collection_name=collection_name, documents=documents)

    def search(self, collection_name: str, query_vector: list, limit: int = 10):
        return self.client.search(collection_name=collection_name, query_vector=query_vector, limit=limit)

    def delete_collection(self, collection_name: str):
        self.client.delete_collection(collection_name=collection_name)