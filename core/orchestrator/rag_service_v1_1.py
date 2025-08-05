import json
from typing import AsyncGenerator

from core.models.request.chat_request import ChatRequest
from core.orchestrator.rag_service_v1 import RAGServiceV1_0

class RAGServiceV1_1(RAGServiceV1_0):
    async def stream_chat(self, req: ChatRequest) -> AsyncGenerator[str, None]:
        try:
            # 1) embedding + router
            vector_question, embedding_time = self.embedding_service.encode(req.question)
            route_info = self.router.route_query(req.question)

            # 2) build prompt và lấy retrieval_time
            prompt, retrieval_time = self._build_prompt(req, vector_question, route_info)

            # 3) (tuỳ chọn) gửi metadata đầu tiên
            meta = {
                "meta": {
                    "embedding_time": embedding_time,
                    "retrieval_time": retrieval_time,
                    "router_result": {
                        "best_route": route_info.best_route,
                        "best_score": route_info.best_score
                    }
                }
            }
            yield json.dumps(meta) + "\n"

            # 4) stream từng token từ inference
            async for token in self.inference_service.generate_answer_stream(prompt):
                yield json.dumps({"token": token}) + "\n"

        except Exception as e:
            err = {"error": str(e)}
            yield json.dumps(err) + "\n"
