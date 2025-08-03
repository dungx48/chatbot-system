import core.router.samples as samples
from core.models.dto.route import Route
from core.router.sematic_router import SemanticRouter
from core.models.dto.router_result_dto import RouterResultDto
from core.common.constant import ConstantRouter

class RoutingService:
    def __init__(self, embedding):
        self.embedding = embedding
        routes = [
            Route(name=ConstantRouter.BUSINESS_ROUTE, samples=samples.business_samples),
            Route(name=ConstantRouter.CHITCHAT_ROUTE, samples=samples.chitchat_samples)
        ]
        self._router = SemanticRouter(self.embedding, routes)

    def route_query(self, query: str) -> RouterResultDto:
        return self._router.guide(query)
