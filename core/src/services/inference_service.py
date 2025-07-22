from typing import Any, Dict
import requests

class InferenceService:
    def __init__(self, inference_api_url: str):
        self.inference_api_url = inference_api_url

    def infer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(self.inference_api_url, json=data)
        response.raise_for_status()
        return response.json()