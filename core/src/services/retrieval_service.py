from typing import Any, Dict
import requests

class RetrievalService:
    def __init__(self, retrieval_api_url: str):
        self.retrieval_api_url = retrieval_api_url

    def fetch_data(self, query: str) -> Dict[str, Any]:
        response = requests.post(f"{self.retrieval_api_url}/retrieve", json={"query": query})
        response.raise_for_status()
        return response.json()