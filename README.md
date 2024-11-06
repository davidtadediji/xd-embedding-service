# XD Embedding Service

A service to compute, store, and retrieve text embeddings using OpenAI, Hugging Face, or Ollama models and Pinecone.

## Features

- **Compute Embeddings**: Utilize OpenAI, Hugging Face, or Ollama models to generate text embeddings.
- **Store Embeddings**: Save embeddings in Pinecone for efficient semantic search.
- **REST API**: Endpoints for embedding documents, searching embeddings, and processing documents from S3.

## Setup

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

    Create a `.env` file in the root directory and add your API keys:

    ```dotenv
    OPENAI_API_KEY=your_openai_api_key
    PINECONE_API_KEY=your_pinecone_api_key
    PINECONE_ENVIRONMENT=your_pinecone_environment
    OLLAMA_MODEL=your_ollama_model
    OLLAMA_BASE_URL=your_ollama_base_url
    S3_ACCESS_KEY=your_s3_access_key
    S3_SECRET_KEY=your_s3_secret_key
    S3_REGION=your_s3_region
    S3_BUCKET=your_s3_bucket
    S3_ENDPOINT=your_s3_endpoint
    LOG_LEVEL=INFO
    ```

5. **Run the application**

    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access the API docs**

    Open your browser and navigate to `http://127.0.0.1:8000/docs` to explore the API endpoints.

## API Endpoints

- `POST /embed`: Embed a single document and store its embedding.
- `POST /search`: Search for relevant documents based on a query.
- `POST /process`: Fetch and process new documents from S3, generating and storing their embeddings.

## License

MIT License
