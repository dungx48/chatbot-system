import re

from core.common.calcu_process_time import measure_time
from core.inference.inference_adapter import get_inference_adapter


class InferenceService:
    def __init__(self, provider: str, api_key: str, model: str, base_url: str = None):
        self.adapter = get_inference_adapter(provider, api_key, model, base_url)

    @measure_time
    def generate_answer(self, prompt: str) -> str:
        raw_answer = self.adapter.generate(prompt)
        think, answer = self.extract_think_and_answer(raw_answer)
        return think, answer

    # Phương thức này để xử lý kết quả trả về từ mô hình
    # Tách (think) và (answer)
    @staticmethod
    def extract_think_and_answer(raw_answer: str):
        import re
        if "<think>" in raw_answer and "</think>" in raw_answer:
            m = re.search(r'<think>(.*?)</think>', raw_answer, flags=re.DOTALL)
            think = m.group(1).strip() if m else ""
            answer = re.sub(r'<think>.*?</think>', '', raw_answer, flags=re.DOTALL).strip()
            return think, answer
        else:
            # Không có think, trả answer bình thường
            return "", raw_answer.strip()