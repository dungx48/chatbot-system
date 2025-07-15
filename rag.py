from vector_db import VectorDatabase
from embeddings import Embeddings


def main():
    vector_db = VectorDatabase(db_type="qdrant")

    embedding = Embeddings(
        model_name="gemini-embedding-exp-03-07", 
        type="gemini"
    )

    print(embedding.encode("Hello, world!"))

if __name__ == "__main__":
    main()