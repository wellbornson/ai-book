from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid
from backend.src.services.session_service import session_service
from backend.src.utils.auth import verify_token


router = APIRouter()


class CreateSessionRequest(BaseModel):
    book_id: str = Field(..., description="ID of the book to chat about")
    initial_context: str = Field("full-book", pattern="^(full-book|selected-text)$", description="Initial query context")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Initial selected text (if initial_context is selected-text)")


class CreateSessionResponse(BaseModel):
    session_id: str
    created_at: datetime
    book_id: str


class SessionResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: Optional[datetime]
    book_id: str


class ChatHistoryItem(BaseModel):
    query: str
    response: str
    timestamp: datetime
    citations: List[str]


@router.post("/sessions", response_model=CreateSessionResponse)
async def create_session(
    request: CreateSessionRequest,
    token: str = Depends(verify_token)
):
    """
    Create a new chat session
    """
    try:
        # Generate a title based on the first few words of the book or context
        title = f"Chat about {request.book_id[:50]}"
        
        # Create session metadata with book info and initial context
        metadata = {
            "book_id": request.book_id,
            "initial_context": request.initial_context,
            "created_with_selected_text": request.selected_text is not None
        }
        
        # Create the session
        db_session = await session_service.create_session(
            title=title,
            metadata=metadata
        )
        
        return CreateSessionResponse(
            session_id=str(db_session.id),
            created_at=db_session.created_at,
            book_id=request.book_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating session: {str(e)}"
        )


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    token: str = Depends(verify_token)
):
    """
    Get session details
    """
    try:
        db_session = await session_service.get_session(session_id)
        if not db_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Extract book_id from metadata
        book_id = db_session.session_metadata.get("book_id", "unknown")
        
        return SessionResponse(
            id=db_session.id,
            title=db_session.title,
            created_at=db_session.created_at,
            updated_at=db_session.updated_at,
            book_id=book_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving session: {str(e)}"
        )


@router.get("/sessions/{session_id}/history", response_model=List[ChatHistoryItem])
async def get_session_history(
    session_id: str,
    token: str = Depends(verify_token)
):
    """
    Get chat history for a session
    """
    try:
        history = await session_service.get_session_history(session_id)
        if history is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Format the history items
        formatted_history = []
        for item in history:
            formatted_history.append(ChatHistoryItem(
                query=item["query"],
                response=item["response"],
                timestamp=item["timestamp"],
                citations=item.get("citations", [])
            ))
        
        return formatted_history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving session history: {str(e)}"
        )