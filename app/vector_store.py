import pinecone
from pinecone.exceptions import NotFoundException
from app.config import settings


class VectorStore:
    def __init__(self):
        # Initialize Pinecone instance
        self.pc = pinecone.Pinecone(
            api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT
        )

        print(self.pc.list_indexes())
        print(settings.PINECONE_INDEX)
        # Check if the index exists, create if it doesn't
        if not any(
            index["name"] == settings.PINECONE_INDEX for index in self.pc.list_indexes()
        ):
            self.pc.create_index(
                name=settings.PINECONE_INDEX,
                dimension=settings.VECTOR_DIMENSION,
                spec={
                    "metric": "cosine",
                    "replicas": 1,
                    "serverless": {
                        "cloud": settings.PINECONE_CLOUD,
                        "region": settings.PINECONE_REGION,
                    },
                },
            )
        try:
            self.index = self.pc.Index(settings.PINECONE_INDEX)
        except NotFoundException as e:
            # Handle the exception, log it, or raise a custom error
            print(f"Error: {e}")
            raise RuntimeError(
                "Pinecone index not found. Please check the index name and configuration."
            )

        self.dimension = settings.VECTOR_DIMENSION

    def upsert_embeddings(self, ids, embeddings, metadata=None, namespace=None):
        self.index.upsert(
            vectors=zip(ids, embeddings, metadata or []), namespace=namespace
        )

    def query_embeddings(self, vector, top_k=10):
        return self.index.query(vector=vector, top_k=top_k, include_metadata=True)
