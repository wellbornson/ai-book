from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from backend.src.services.rag_service import rag_service
from backend.src.utils.auth import verify_token
from backend.src.utils.error_handler import QueryProcessingError, ExternalServiceError


router = APIRouter()


class QueryRequest(BaseModel):
    session_id: str = Field(..., description="Session ID for the conversation")
    query_text: str = Field(..., min_length=1, max_length=1000, description="The user's question")
    query_mode: str = Field("full-book", pattern="^(full-book|selected-text)$", description="Query mode: full-book or selected-text")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Text selected by user (required if query_mode is selected-text)")


class Citation(BaseModel):
    source_location: str
    content: str


class QueryResponse(BaseModel):
    response_id: str
    response_text: str
    citations: List[Citation]
    query_mode: str


@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    token: str = Depends(verify_token)
):
    """
    Submit a query about the book content
    """
    try:
        # Validate request based on query mode
        if request.query_mode == "selected-text" and not request.selected_text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="selected_text is required when query_mode is 'selected-text'"
            )
        
        # Process the query through the RAG service
        result = rag_service.process_query(
            query_text=request.query_text,
            query_mode=request.query_mode,
            session_id=request.session_id,
            selected_text=request.selected_text
        )
        
        # Format the response
        formatted_response = QueryResponse(
            response_id=result["response_id"],
            response_text=result["response_text"],
            citations=[
                Citation(
                    source_location=citation["source_location"],
                    content=citation["content"]
                ) 
                for citation in result["citations"]
            ],
            query_mode=result["query_mode"]
        )
        
        return formatted_response
        
    except QueryProcessingError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": {
                    "code": e.error_code,
                    "message": e.message
                }
            }
        )
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": {
                    "code": e.error_code,
                    "message": e.message
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal server error occurred"
                }
            }
        )


class SelectTextRequest(BaseModel):
    selected_text: str = Field(..., max_length=5000, description="The text selected by the user")


class SelectTextResponse(BaseModel):
    session_id: str
    selected_text: str
    query_mode: str = "selected-text"


@router.post("/sessions/{session_id}/select-text", response_model=SelectTextResponse)
async def select_text_for_session(
    session_id: str,
    request: SelectTextRequest,
    token: str = Depends(verify_token)
):
    """
    Update session to use selected text mode
    """
    # In a real implementation, we would update the session in the database
    # For now, we'll just return the selected text and session info
    
    # Basic validation
    if not request.selected_text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Selected text cannot be empty"
        )
    
    # In a real implementation, we would:
    # 1. Verify the session exists
    # 2. Update the session's query mode to "selected-text"
    # 3. Store the selected text with the session
    # 4. Return the updated session info
    
    return SelectTextResponse(
        session_id=session_id,
        selected_text=request.selected_text,
        query_mode="selected-text"
    )