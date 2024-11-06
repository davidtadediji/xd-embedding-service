# XD Embedding Service

## Overview

The **XD Embedding Service** is a powerful solution for computing, storing, and retrieving text embeddings. It leverages models from OpenAI, Hugging Face, or Ollama and utilizes Pinecone for efficient semantic search. Additionally, it integrates with AWS S3 for document management and supports Neo4j for graph-based data representation.

## Features

- **Compute Embeddings**: Generate text embeddings using OpenAI, Hugging Face, or Ollama models.
- **Store Embeddings**: Efficiently store embeddings in Pinecone for fast and scalable semantic search.
- **REST API**: Comprehensive API endpoints for embedding documents, searching embeddings, and processing documents from S3.
- **Document Processing**: Fetch and process documents from AWS S3, split them into manageable chunks, and store their embeddings.
- **Logging**: Detailed logging for monitoring and debugging purposes.
- **Configuration Management**: Easily manage environment variables using `.env` files.

## Setup

### Prerequisites

- Python 3.12
- Git
- AWS Account (for S3 access)
- Pinecone Account
- Neo4j Instance (optional)

### Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/xd-embedding-service.git
    cd xd-embedding-service
    ```

2. **Create a virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**

    Create a `.env` file in the root directory and add your API keys and configuration details:

    ```dotenv
    # OpenAI API Key
    OPENAI_API_KEY=your_openai_api_key_here

    # Pinecone Configuration
    PINECONE_API_KEY=your_pinecone_api_key
    PINECONE_ENVIRONMENT=your_pinecone_environment
    PINECONE_INDEX=xd-embedding-index
    VECTOR_DIMENSION=your_vector_dimension
    PINECONE_CLOUD=aws
    PINECONE_REGION=us-east-1

    # Ollama Configuration
    OLLAMA_EMDEDDING_MODEL=mxbai-embed-large
    OLLAMA_BASE_URL=http://localhost:11434

    # Hugging Face Embedding Model
    HUGGINGFACE_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

    # AWS S3 Configuration
    S3_ACCESS_KEY=your_s3_access_key
    S3_SECRET_KEY=your_s3_secret_key
    S3_REGION=your_s3_region
    S3_BUCKET=your_s3_bucket
    S3_ENDPOINT=https://your_s3_endpoint_here

    # Logging
    LOG_LEVEL=DEBUG
    ```

5. **Run the application**

    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access the API Documentation**

    Open your browser and navigate to `http://127.0.0.1:8000/docs` to explore and interact with the API endpoints.

## API Endpoints

### Embed a Single Document

- **Endpoint**: `POST /api/v1/embed-file`
- **Description**: Embed a single document and store its embedding.
- **Request Body**:
    ```json
    {
        "title": "Document Title",
        "text": "The content of the document.",
        "metadata": {
            "author": "Author Name",
            "date": "2023-10-13"
        }
    }
    ```
- **Response**:
    ```json
    {
        "embedding_id": "single_chunk_unique_id",
        "status": "success"
    }
    ```

### Embed Documents from an S3 Bucket

- **Endpoint**: `POST /api/v1/embed-bucket`
- **Description**: Fetch and process documents from an S3 bucket, generating and storing their embeddings.
- **Request Body** (optional):
    ```json
    {
        "prefix": "optional/prefix/path/"
    }
    ```
- **Response**:
    ```json
    {
        "status": "success",
        "stats": {
            "processed": 10,
            "skipped": 2,
            "chunks": 50
        }
    }
    ```

### Search for Documents

- **Endpoint**: `POST /api/v1/search`
- **Description**: Search for relevant documents based on a query.
- **Request Body**:
    ```json
    {
        "query": "your search query",
        "top_k": 10,
        "model": "mxbai-embed-large"
    }
    ```
- **Response**:
    ```json
    {
        "results": [
            {
                "id": "chunk_id_1",
                "score": 0.95,
                "metadata": {
                    "source_key": "document_key_1",
                    "chunk_index": 0,
                    "content": "A preview of the content..."
                }
            }
            // More results...
        ]
    }
    ```

## Logging

The service uses Python's standard logging library. The logging level can be configured via the `LOG_LEVEL` environment variable in the `.env` file. Logs are output to the console with timestamps, logger names, log levels, and messages.

## Configuration

All configurations are managed through environment variables. Ensure that the `.env` file is properly set up before running the application. Sensitive information should be kept secure and **not** committed to version control.

### Environment Variables

- **AWS Configuration**
    ```dotenv
    S3_ACCESS_KEY=your_s3_access_key
    S3_SECRET_KEY=your_s3_secret_key
    S3_REGION=your_s3_region
    S3_BUCKET=your_s3_bucket
    S3_ENDPOINT=https://your_s3_endpoint_here
    ```

- **Database Configuration**
    ```dotenv
    DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
    ```

- **Logging**
    ```dotenv
    LOG_LEVEL=DEBUG
    ```

- **Neo4j Configuration**
    ```dotenv
    NEO4J_URI=neo4j+s://your_neo4j_uri_here
    NEO4J_USERNAME=your_neo4j_username_here
    NEO4J_PASSWORD=your_neo4j_password_here
    ```

- **OpenAI API Key**
    ```dotenv
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear and descriptive messages.
4. Push to your forked repository.
5. Open a pull request detailing your changes.

## License

This project is licensed under the [MIT License](LICENSE).
