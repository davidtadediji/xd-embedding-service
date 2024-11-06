import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    VECTOR_DIMENSION: int
    PINECONE_INDEX: str = "xd-embedding-index"
    PINECONE_CLOUD: str = "aws"
    PINECONE_REGION: str = "us-east-1"

    # Ollama Configurations
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # AWS Configuration
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str
    S3_BUCKET: str
    S3_ENDPOINT: str

    # Application Settings
    LOG_LEVEL: str  # Added LOG_LEVEL

    OLLAMA_EMDEDDING_MODEL: str = os.getenv(
        "OLLAMA_EMBEDDING_MODEL", "mxbai-embed-large"
    )
    OPENAI_EMBEDDING_MODEL: str = os.getenv(
        "OPENAI_EMBEDDING_MODEL", "default-openai-model"
    )
    HUGGINGFACE_EMBEDDING_MODEL: str = os.getenv(
        "HUGGINGFACE_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    class ConfigDict:  # Changed to ConfigDict
        env_file = ".env"


settings = Settings()
