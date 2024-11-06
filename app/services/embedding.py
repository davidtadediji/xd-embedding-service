from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings
import logging
import time
from requests.exceptions import RequestException
from typing import List

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self.openai_embed = OpenAIEmbeddings(model=settings.OPENAI_EMBEDDING_MODEL)
        self.hf_embed = HuggingFaceEmbeddings(
            model_name=settings.HUGGINGFACE_EMBEDDING_MODEL
        )
        self.ollama_embed = OllamaEmbeddings(
            model=settings.OLLAMA_EMDEDDING_MODEL, base_url=settings.OLLAMA_BASE_URL
        )

    def get_openai_embeddings(self, text: str) -> List[float]:
        if not text.strip():
            logger.warning("Empty or whitespace-only text received for embedding.")
            return self._zero_vector()

        retries = 3
        for attempt in range(retries):
            try:
                embedding = self.openai_embed.embed_query(text)
                if not embedding:
                    logger.warning("Received empty embedding from OpenAI.")
                    return self._zero_vector()
                return embedding
            except RequestException as e:
                logger.error(f"RequestException on attempt {attempt + 1}: {str(e)}")
                time.sleep(2**attempt)  # Exponential backoff
            except Exception as e:
                logger.error(f"Unexpected error generating OpenAI embeddings: {str(e)}")
                break
        logger.error("Failed to generate valid embeddings after multiple attempts.")
        return self._zero_vector()

    def get_huggingface_embeddings(self, text: str) -> list:
        return self.hf_embed.embed_query(text)

    def get_ollama_embeddings(self, text: str) -> list:
        return self.ollama_embed.embed_query(text)

    def _zero_vector(self) -> List[float]:
        """
        Generate a zero vector based on the expected embedding dimension.

        Returns:
            List[float]: A zero vector.
        """
        return [0.0] * settings.VECTOR_DIMENSION
