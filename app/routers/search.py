from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.services.embedding import EmbeddingService
from app.vector_store import VectorStore
from app.utils.logger import logger
from app.services.dependencies import get_embedding_service, get_vector_store
from app.models.search_query import SearchQuery

router = APIRouter()


@router.post("/search")
def search_documents(
    query: SearchQuery,
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: VectorStore = Depends(get_vector_store),
):
    """
    Endpoint to search for documents based on a query.

    Args:
        query (SearchQueryModel): The search query parameters.
        embedding_service (EmbeddingService): Singleton instance of EmbeddingService.
        vector_store (VectorStore): Singleton instance of VectorStore.

    Returns:
        dict: Search results containing matching documents.
    """
    try:
        query_embedding = embedding_service.get_openai_embeddings(query.query)
        results = vector_store.query_embeddings(
            vector=query_embedding, top_k=query.top_k
        )
        return {"results": results.matches}
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
