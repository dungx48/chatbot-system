from core.embedding.embedding_service import EmbeddingService
from core.inference.inference_service import InferenceService
from core.models.request.chat_request import ChatRequest
from core.models.dto.router_result_dto import RouterResultDto
from core.retrieval.retrieval_service import RetrievalService
from core.router.routing_service import RoutingService
from core.common.constant import ConstantRouter
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

        self.router = RoutingService(
            embedding=self.embedding_service
        )

    async def chat(self, req: ChatRequest) -> dict:
        """
        :param question: The question to respond to.
        :return: A dictionary containing the answer.

        embedding question -> retrieve relevant context -> generate answer
        
        """
        try:
            # Embedding question
            vector_question, embedding_time = self.embedding_service.encode(req.question)

            # Get promt from input
            route_info = self.router.route_query(req.question)
            prompt, retrieval_time = self._build_prompt(req, vector_question, route_info)

            # Generate answer
            gene_result, inference_time = self.inference_service.generate_answer(prompt)

            return {
                "answer": gene_result.answer,
                "think": gene_result.think,
                "process_times": {
                    "embedding": embedding_time,
                    "retrieval": retrieval_time,
                    "inference": inference_time
                },
                "router_result": {
                    "best_route": route_info.best_route,
                    "best_score": route_info.best_score
                },
                "embedded_question": vector_question
            }
        except Exception as e:
            print(f"Error in RAGService: {e}")
            raise
    
    def _build_prompt(self, req: ChatRequest, vector_question:list[float], route_info: RouterResultDto) -> str:
        if(route_info.best_route == ConstantRouter.CHITCHAT_ROUTE or route_info.best_score < settings.SCORE_ROUTER_THRESHOLD):
            prompt = f"""Context:\n{req.question}"""

        elif(route_info.best_route == ConstantRouter.BUSINESS_ROUTE):
            # Retrieve relevant context
            retrieval_results, retrieval_time = self.retrieval_service.search(vector_question)
            retrieval_texts = [result.payload["text"] for result in retrieval_results if result.payload.get("text")]
            context = " ".join(retrieval_texts)
            prompt = f"""Context:\n{context}\n\nUser prompt: {req.user_prompt}"""
        
        return prompt, retrieval_time