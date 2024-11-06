from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import uuid
from app.models.document import Document

from app.services.embedding import EmbeddingService
from app.vector_store import VectorStore
from app.services.dependencies import (
    get_embedding_service,
    get_vector_store,
    get_document_tracker,
)
from app.utils.logger import logger
from app.services.document_tracker import DocumentTracker

router = APIRouter()


@router.post("/embed-file")
def embed_document(
    document: Document,
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: VectorStore = Depends(get_vector_store),
    document_tracker: DocumentTracker = Depends(get_document_tracker),
):
    """
    Endpoint to embed a single document and store its embedding.

    Args:
        document (DocumentModel): The document to embed.
        embedding_service (EmbeddingService): Singleton instance of EmbeddingService.
        vector_store (VectorStore): Singleton instance of VectorStore.
        document_tracker (DocumentTracker): Singleton instance of DocumentTracker.

    Returns:
        dict: Embedding ID and status of the operation.
    """
    try:
        # Check if the document has already been processed
        if document_tracker.is_processed(document.title):
            raise HTTPException(status_code=400, detail="Document has already been processed.")

        embedding = embedding_service.get_openai_embeddings(document.text)
        chunk_id = f"single_chunk_{uuid.uuid4()}"
        metadata = {
            "source_key": "manual",
            "chunk_index": 0,
            "total_chunks": 1,
            "content_preview": document.text[:200],
            **document.metadata,
        }
        vector_store.upsert_embeddings(
            ids=[chunk_id], embeddings=[embedding], metadata=[metadata]
        )
        document_tracker.mark_as_processed(
            document.title
        )  # Mark the document as processed using the title
        return {"embedding_id": chunk_id, "status": "success"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error embedding document: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
