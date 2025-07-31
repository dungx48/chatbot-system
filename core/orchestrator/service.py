from core.embedding.embedding_service import EmbeddingService
from core.inference.inference_service import InferenceService
from core.models.request.chat_request import ChatRequest
from core.retrieval.retrieval_service import RetrievalService

from core.common.config import settings


class RAGService:
    def __init__(self):
        """
        :param embedding_model: Model used for embedding questions.
        :param retrieval_service: Service used for retrieving relevant context.
        """
        self.embedding_service = EmbeddingService(
            adapter_type=settings.EMBEDDING_SERVICE,
            model_name=settings.EMBEDDING_MODEL_NAME
        )

        self.retrieval_service = RetrievalService()

        self.inference_service = InferenceService(
            provider="ollama",
            api_key="",
            model=settings.LLM_MODEL_NAME,
            base_url=settings.LLM_URL_HOST
        )

    async def chat(self, req: ChatRequest) -> dict:
        """
        :param question: The question to respond to.
        :return: A dictionary containing the answer.

        embedding question -> retrieve relevant context -> generate answer
        
        """

        # Embedding question
        vector_question, process_time_embedding = self.embedding_service.encode(req.question)

        # Retrieve relevant context
        retrieval_results, process_time_retrieval = self.retrieval_service.search(vector_question)

        # Generate answer
        retrieval_texts = [result.payload["text"] for result in retrieval_results if result.payload.get("text")]
        context = " ".join(retrieval_texts)
        prompt = f"""Context:\n{context}\n\nUser prompt: {req.user_prompt}"""
        (think, answer), process_time_inference = self.inference_service.generate_answer(prompt)

        return {
            "answer": answer,
            "think": think,
            "process_times": {
                "embedding": process_time_embedding,
                "retrieval": process_time_retrieval,
                "inference": process_time_inference
            },
            "embedded_question": vector_question
        }