from core.common.calcu_process_time import measure_time
from core.inference.inference_adapter import get_inference_adapter


class InferenceService:
    def __init__(self, provider: str, api_key: str, model: str, base_url: str = None):
        self.adapter = get_inference_adapter(provider, api_key, model, base_url)

    @measure_time
    def generate_answer(self, prompt: str) -> str:
        return self.adapter.generate(prompt)