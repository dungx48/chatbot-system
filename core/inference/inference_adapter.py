import httpx
import json

# import google.generativeai as genai
from openai import OpenAI
from common.config import settings

class BaseInferenceAdapter:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
    async def stream_generate(self, prompt: str):
        """
        Async generator: mỗi lần yield về một đoạn text.
        """
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
    
    async def stream_generate(self, prompt: str):
        # gọi stream=True sẽ trả về AsyncIterable[chunk]
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        async for chunk in stream:
            # chunk.choices[0].delta.message.content hoặc delta.content
            token = chunk.choices[0].delta.get("content", "")
            if token:
                yield token

# class GeminiInferenceAdapter(BaseInferenceAdapter):
#     def __init__(self, api_key: str, model: str):
#         self.client = genai.Client(api_key=api_key)
#         self.model = model

#     def generate(self, prompt: str) -> str:
#         response = self.client.generate_content(self.model, prompt=prompt)
#         return response.text

class OllamaInferenceAdapter(BaseInferenceAdapter):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip('/')
        self.model = model

    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": settings.STREAM_OUTPUT
        }
        with httpx.Client(timeout=1200) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            # Phải đọc từng dòng, mỗi dòng là 1 object JSON nhỏ
            result = ""
            for line in resp.iter_lines():
                if line:
                    data = json.loads(line)
                    result += data.get("response", "")
            return result
        
    async def stream_generate(self, prompt: str):
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }
        async with httpx.AsyncClient(timeout=1200) as client:
            async with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        if chunk:
                            yield chunk

def get_inference_adapter(provider: str, api_key: str, model: str, base_url: str = None) -> BaseInferenceAdapter:
    if provider.lower() == "openai":
        return OpenAIInferenceAdapter(api_key, model)
    # elif provider.lower() == "gemini":
    #     return GeminiInferenceAdapter(api_key, model)
    elif provider == "ollama":
        if not base_url:
            raise ValueError("base_url is required for OllamaInferenceAdapter")
        print(f"Using OllamaInferenceAdapter with model: {model}")
        return OllamaInferenceAdapter(base_url, model)
    else:
        raise ValueError(f"Provider '{provider}' is not supported!")