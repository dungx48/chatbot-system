import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from router import Route, SemanticRouter

from samples import product_samples, chitchat_samples
from embeddings import Embeddings

embedding = Embeddings(
    type="sentence_transformers", 
    model_name="BAAI/bge-m3"
)

productRoute = Route(
    name="productRoute",
    samples=product_samples
)

chitchatRoute = Route(
    name="chitchatRoute",
    samples=chitchat_samples
)

router = SemanticRouter(
    embedding=embedding,
    routers=[
        productRoute, 
        chitchatRoute
    ]
)


# Example usage
query = "thẻ dùng trong bao lâu thì được cấp lại?"
print(router.guide(query))
