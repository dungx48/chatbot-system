# core/common/config.py
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = Field(..., env="PORT")
    TOP_K_RETRIEVAL: int = Field(3, env="TOP_K_RETRIEVAL")
    EMBEDDING_SERVICE: str = Field(..., env="EMBEDDING_SERVICE")
    EMBEDDING_MODEL_NAME: str = Field(..., env="EMBEDDING_MODEL_NAME")
    QDRANT_URL: str = Field(..., env="QDRANT_URL")
    QDRANT_COLLECTION_NAME: str = Field(..., env="QDRANT_COLLECTION_NAME")
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    WIKI_JS_URL: str = Field(..., env="WIKI_JS_URL")
    LLM_URL_HOST: str = Field(..., env="LLM_URL_HOST")
    LLM_MODEL_NAME: str = Field(..., env="LLM_MODEL_NAME")
    STREAM_OUTPUT: bool = Field(True, env="STREAM_OUTPUT")
    SCORE_ROUTER_THRESHOLD: float = Field(..., env="SCORE_ROUTER_THRESHOLD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Khởi tạo global settings dùng ở toàn app
settings = Settings()
