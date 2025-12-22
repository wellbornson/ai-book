from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional
from backend.src.services.ingestion_service import ingestion_service
from backend.src.utils.auth import verify_token


router = APIRouter()


class IngestBookRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the book")
    author: str = Field(..., min_length=1, max_length=255, description="Author of the book")
    format: str = Field(..., pattern="^(pdf|txt|epub)$", description="Format of the book content")


class IngestBookResponse(BaseModel):
    book_id: str
    title: str
    status: str
    message: str


@router.post("/books/ingest", response_model=IngestBookResponse)
async def ingest_book(
    file: UploadFile = File(..., description="Book file to ingest"),
    title: str = Form(..., description="Title of the book"),
    author: str = Form(..., description="Author of the book"),
    token: str = Depends(verify_token)
):
    """
    Ingest a book for RAG processing
    """
    try:
        # Validate file type
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['pdf', 'txt']:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unsupported file format: {file_ext}. Only PDF and TXT are supported."
            )
        
        # Save the uploaded file temporarily
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Process the book ingestion
            result = ingestion_service.ingest_book(
                file_path=temp_file_path,
                title=title,
                author=author
            )
            
            return IngestBookResponse(
                book_id=result["book_id"],
                title=result["title"],
                status=result["status"],
                message=result["message"]
            )
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting book: {str(e)}"
        )


class GetBookResponse(BaseModel):
    id: str
    title: str
    author: str
    chunk_count: int
    created_at: str


@router.get("/books/{book_id}", response_model=GetBookResponse)
async def get_book(
    book_id: str,
    token: str = Depends(verify_token)
):
    """
    Get book information
    """
    # In a real implementation, we would retrieve the book from the database
    # For now, we'll return a placeholder response
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get book endpoint not yet implemented"
    )