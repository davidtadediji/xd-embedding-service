from typing import List, Dict

from app.services.document_fetcher import fetch_parsed_documents
from app.services.document_tracker import DocumentTracker
from app.services.embedding import EmbeddingService
from app.vector_store import VectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.utils.logger import logger


class DocumentProcessor:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        document_tracker: DocumentTracker,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.document_tracker = document_tracker
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def process_documents(self, prefix: str = "") -> Dict[str, int]:
        """
        Process new documents from S3 and store their embeddings in Pinecone.
        Returns statistics about the processing.
        """
        stats = {"processed": 0, "skipped": 0, "chunks": 0}

        # Get list of processed documents
        processed_docs = self.document_tracker.get_processed_documents()

        # Fetch new documents
        documents = fetch_parsed_documents(prefix, processed_docs)

        for doc in documents:
            try:
                # Split document into chunks
                chunks = self.text_splitter.split_text(doc["content"])

                if not chunks:
                    logger.warning(f"No content to process for document: {doc['key']}")
                    stats["skipped"] += 1
                    continue

                # Process each chunk
                embeddings = []
                chunk_ids = []
                metadata_list = []

                for i, chunk in enumerate(chunks):
                    print(i)
                    logger.debug(f"Processing chunk {i} of document {doc['key']}")
                    # Generate embedding
                    embedding = self.embedding_service.get_openai_embeddings(chunk)

                    # Validate embedding
                    if not self._is_valid_embedding(embedding):
                        logger.warning(
                            f"Invalid embedding for chunk {i} of document {doc['key']}. Skipping."
                        )
                        stats["skipped"] += 1
                        continue

                    # Prepare metadata
                    metadata = {
                        "source_key": doc["key"],
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "content": chunk[:200],  # Store preview of content
                    }

                    chunk_ids.append(f"{doc['key']}_chunk_{i}")
                    embeddings.append(embedding)
                    metadata_list.append(metadata)

                if embeddings:
                    # Store embeddings in Pinecone
                    self.vector_store.upsert_embeddings(
                        ids=chunk_ids, embeddings=embeddings, metadata=metadata_list
                    )
                    logger.info(
                        f"Upserted {len(embeddings)} embeddings for document: {doc['key']}"
                    )
                else:
                    logger.warning(
                        f"No valid embeddings to upsert for document: {doc['key']}"
                    )

                # Mark document as processed
                self.document_tracker.mark_as_processed(doc["key"])

                stats["processed"] += 1
                stats["chunks"] += len(embeddings)
                logger.info(
                    f"Processed document: {doc['key']} into {len(embeddings)} valid chunks"
                )
            except Exception as e:
                logger.error(f"Error processing document {doc['key']}: {str(e)}")
                stats["skipped"] += 1

        return stats

    def _is_valid_embedding(self, embedding: List[float]) -> bool:
        """
        Validate that the embedding contains at least one non-zero value.

        Args:
            embedding (List[float]): The embedding vector to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return any(value != 0.0 for value in embedding)
