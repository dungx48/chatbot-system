import httpx

import google.generativeai as genai
from openai import OpenAI


class BaseInferenceAdapter:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

class OpenAIInferenceAdapter(BaseInferenceAdapter):
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

class GeminiInferenceAdapter(BaseInferenceAdapter):
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.generate_content(self.model, prompt=prompt)
        return response.text

class OllamaInferenceAdapter(BaseInferenceAdapter):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip('/')
        self.model = model

    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        with httpx.Client(timeout=1200) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["response"]

def get_inference_adapter(provider: str, api_key: str, model: str, base_url: str = None) -> BaseInferenceAdapter:
    if provider.lower() == "openai":
        return OpenAIInferenceAdapter(api_key, model)
    elif provider.lower() == "gemini":
        return GeminiInferenceAdapter(api_key, model)
    elif provider == "ollama":
        if not base_url:
            raise ValueError("base_url is required for OllamaInferenceAdapter")
        return OllamaInferenceAdapter(base_url, model)
    else:
        raise ValueError(f"Provider '{provider}' is not supported!")