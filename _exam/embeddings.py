from openai import OpenAI
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai


load_dotenv()

class Embeddings:
    def __init__(self, model_name, type):
        if not model_name or str(model_name).strip() == "":
            model_name = "BAAI/bge-m3"
        self.model_name = model_name
        self.type = type
        if type == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif type == "sentence_transformers":
            self.client = SentenceTransformer(model_name)
        elif type == "gemini":
            self.client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )

    def encode(self, doc):
        if self.type == "openai":
            return self.client.embeddings.create(
                input=doc,
                model=self.model_name
            ).data[0].embedding
        elif self.type == "sentence_transformers":
            return self.client.encode(doc)
        elif self.type == "gemini":
            return self.client.models.embed_content(
                model=self.model_name,
                contents=doc
            ).embeddings[0].values
