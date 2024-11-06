import boto3
from app.config import settings
from app.utils.logger import logger  # Assuming logger is available for logging

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name=settings.S3_REGION,
)


def fetch_parsed_documents(prefix="", processed_documents=None):
    """Fetch new parsed documents from S3 bucket."""
    if processed_documents is None:
        processed_documents = []
    documents = []
    response = s3_client.list_objects_v2(Bucket=settings.S3_BUCKET, Prefix=prefix)

    for obj in response.get("Contents", []):
        file_key = obj["Key"]
        if file_key in processed_documents:
            logger.info(f"Skipping already processed document: {file_key}")  # Log the skipped document
            continue  # Skip already processed documents

        file_obj = s3_client.get_object(Bucket=settings.S3_BUCKET, Key=file_key)
        content = file_obj["Body"].read().decode("utf-8")
        documents.append(
            {"key": file_key, "content": content}
        )  # Store key with content
        print(f"Fetched document: {file_key}")
    return documents
