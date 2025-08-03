from typing import List, Union
import numpy as np

from core.models.dto.router_result_dto import RouterResultDto

class SemanticRouter:
    def __init__(self, embedding, routers: List):
        """
            :param embedding: một object có method .encode(texts) 
                            trả về np.ndarray hoặc tuple (np.ndarray, ...)
            :param routers:  list các Route, mỗi Route có thuộc tính .name và .samples (List[str])
        """
        self.embedding = embedding
        self.routers = routers
        self.routes_embeddings: dict[str, np.ndarray] = {}

        for route in self.routers:
            # 1) Lấy raw embeddings shape (n_samples, dim)
            embs = self._encode(route.samples)

            # 2) Chuẩn hoá từng sample (hàng) để tính cosine
            norms = np.linalg.norm(embs, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            self.routes_embeddings[route.name] = embs / norms
            
    def _encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        result = self.embedding.encode(texts)
        arr = result[0] if isinstance(result, tuple) else result
        return np.array(arr, dtype=float)
    
    def guide(self, query: str) -> RouterResultDto:
        """
        Trả về (best_score, best_route_name):
        best_score = max cosine similarity giữa query và bất kỳ sample nào trong route.
        """
        # Encode + normalize query
        q = self._encode(query)
        q_norm = np.linalg.norm(q)
        if q_norm > 0:
            q = q / q_norm

        best_score, best_route = -1.0, None
        for name, embs in self.routes_embeddings.items():
            # embs: (n_samples, dim), q: (dim,)
            sims = embs.dot(q)         # mảng shape (n_samples,)
            max_sim = float(np.max(sims))
            if max_sim > best_score:
                best_score, best_route = max_sim, name
        
        router_result_dto = {
            "best_route":best_route,
            "best_score":best_score
        }

        return RouterResultDto(**router_result_dto)