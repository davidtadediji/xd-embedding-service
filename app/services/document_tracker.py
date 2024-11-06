from app.vector_store import VectorStore
from app.utils.logger import logger


class DocumentTracker:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.processed_namespace = "processed_docs"

    def mark_as_processed(self, document_key: str):
        """Mark a document as processed in Pinecone."""
        try:
            # Ensure at least one non-zero value in the vector
            placeholder_vector = [1.0] + [0.0] * (self.vector_store.dimension - 1)
            self.vector_store.upsert_embeddings(
                ids=[document_key],
                embeddings=[placeholder_vector],  # Updated placeholder vector
                metadata=[{"processed": True, "type": "tracker"}],
                namespace=self.processed_namespace,
            )
        except Exception as e:
            logger.error(
                f"Error marking document {document_key} as processed: {str(e)}"
            )
            raise  # Re-raise the exception after logging

    def is_processed(self, document_key: str) -> bool:
        """Check if a document has been processed."""
        try:
            results = self.vector_store.index.fetch(
                [document_key], namespace=self.processed_namespace
            )
            return bool(results.get("vectors", {}))
        except Exception as e:
            logger.error(f"Error checking if document {document_key} is processed: {str(e)}")
            return False  # Return False if an error occurs

    def get_processed_documents(self) -> list:
        """Get all processed document keys."""
        try:
            results = self.vector_store.index.query(
                vector=[0] * self.vector_store.dimension,
                namespace=self.processed_namespace,
                top_k=10000,
                include_metadata=True,
            )
            return [match.id for match in results.matches]
        except Exception as e:
            logger.error(f"Error retrieving processed documents: {str(e)}")
            return []  # Return an empty list if an error occurs
