import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer
# import google.generativeai as genai

class BaseEmbeddingAdapter:
    def get_embedding(self, doc):
        raise NotImplementedError("Phải override hàm này")

class OpenAIAdapter(BaseEmbeddingAdapter):
    def __init__(self, model_name=None):
        self.model_name = model_name or "text-embedding-ada-002"
        try:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception as e:
            print("Không khởi tạo được OpenAI: %s" % e)
    def get_embedding(self, doc):
        try:
            result = self.client.embeddings.create(
                input=doc, model=self.model_name
            )
            return result.data[0].embedding
        except Exception as e:
            print("OpenAI embedding error: %s" % e)

class SentenceTransformerAdapter(BaseEmbeddingAdapter):
    def __init__(self, model_name=None):
        self.model_name = model_name or "BAAI/bge-m3"
        try:
            self.client = SentenceTransformer(self.model_name)
        except Exception as e:
            print("Không khởi tạo được SentenceTransformer: %s" % e)
    def get_embedding(self, doc):
        try:
            return self.client.encode(doc)
        except Exception as e:
            print("SentenceTransformer embedding error: %s" % e)

# class GeminiAdapter(BaseEmbeddingAdapter):
#     def __init__(self, model_name=None):
#         self.model_name = model_name or "models/embedding-001"
#         try:
#             self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
#         except Exception as e:
#             print("Không khởi tạo được Gemini: %s" % e)
#     def get_embedding(self, doc):
#         try:
#             response = self.client.models.embed_content(
#                 model=self.model_name,
#                 contents=doc
#             )
#             return response.embeddings[0].values
#         except Exception as e:
#             print("Gemini embedding error: %s" % e)

def get_adapter(adapter_type, model_name=None):
    adapter_type = adapter_type.lower()
    if adapter_type == "openai":
        return OpenAIAdapter(model_name)
    elif adapter_type == "sentence_transformers":
        return SentenceTransformerAdapter(model_name)
    # elif adapter_type == "gemini":
    #     return GeminiAdapter(model_name)
    else:
        print(f"Không hỗ trợ adapter: {adapter_type}")
