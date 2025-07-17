from typing import List
import numpy as np


class Route:
    def __init__(self, name:str = None, samples:List = []):
        self.name = name
        self.samples = samples

class SemanticRouter:
    def __init__(self, embedding, routers):
        self.embedding = embedding
        self.routers = routers
        self.routesEmbeddings = {}

        for route in self.routers:
            self.routesEmbeddings[route.name] = self.embedding.encode(route.samples)
    
    def guide(self, query: str): # cosine similarity
        query_embedding = self.embedding.encode([query])
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        scores = []

        for route in self.routers:
            routesEmbeddings = self.routesEmbeddings[route.name] / np.linalg.norm(self.routesEmbeddings[route.name])
            score = np.mean(np.dot(routesEmbeddings, query_embedding.T).flatten())
            scores.append((score, route.name))
        scores.sort(reverse=True)

        return scores[0]

