from fastapi import Depends
from app.services.embedding import EmbeddingService
from app.vector_store import VectorStore
from app.services.document_tracker import DocumentTracker
from app.document_processor import DocumentProcessor

# Singleton instances initialized as None
_embedding_service_instance = None
_vector_store_instance = None
_document_tracker_instance = None
_document_processor_instance = None


def get_embedding_service() -> EmbeddingService:
    """
    Provides a singleton instance of EmbeddingService.
    """
    global _embedding_service_instance
    if _embedding_service_instance is None:
        _embedding_service_instance = EmbeddingService()
    return _embedding_service_instance


def get_vector_store() -> VectorStore:
    """
    Provides a singleton instance of VectorStore.
    """
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance


def get_document_tracker(
    vector_store: VectorStore = Depends(get_vector_store),
) -> DocumentTracker:
    """
    Provides a singleton instance of DocumentTracker.
    """
    global _document_tracker_instance
    if _document_tracker_instance is None:
        _document_tracker_instance = DocumentTracker(vector_store=vector_store)
    return _document_tracker_instance


def get_document_processor(
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: VectorStore = Depends(get_vector_store),
    document_tracker: DocumentTracker = Depends(get_document_tracker),
) -> DocumentProcessor:
    """
    Provides a singleton instance of DocumentProcessor.
    """
    global _document_processor_instance
    if _document_processor_instance is None:
        _document_processor_instance = DocumentProcessor(
            embedding_service=embedding_service,
            vector_store=vector_store,
            document_tracker=document_tracker,
        )
    return _document_processor_instance
