from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.document_processor import DocumentProcessor
from app.services.dependencies import get_document_processor
from app.utils.logger import logger

router = APIRouter()


@router.post("/embed-bucket")
def process_documents(
    prefix: Optional[str] = "",
    document_processor: DocumentProcessor = Depends(get_document_processor),
):
    """
    Endpoint to process documents and generate embeddings.

    Args:
        prefix (Optional[str]): Optional prefix to filter documents.
        document_processor (DocumentProcessor): Singleton instance of DocumentProcessor.

    Returns:
        dict: Status and statistics of the processing operation.
    """
    try:
        print("processing documents")
        stats = document_processor.process_documents(prefix)
        return {"status": "success", "stats": stats}
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
