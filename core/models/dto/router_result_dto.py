from pydantic import BaseModel

class RouterResultDto(BaseModel):
    best_route: str
    best_score: float
