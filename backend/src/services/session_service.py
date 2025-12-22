from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from backend.src.models.chat_session import ChatSession
from backend.src.models.user_query import UserQuery
from backend.src.models.generated_response import GeneratedResponse
from backend.src.config.database import async_session
import uuid


class SessionService:
    """
    Service for managing chat sessions and history
    """
    
    def __init__(self):
        pass
    
    async def create_session(self, title: str, user_id: Optional[str] = None, metadata: Optional[Dict] = None) -> ChatSession:
        """
        Create a new chat session
        """
        async with async_session() as session:
            db_session = ChatSession(
                user_id=user_id,
                title=title,
                session_metadata=metadata or {}
            )
            session.add(db_session)
            await session.commit()
            await session.refresh(db_session)
            return db_session
    
    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get a chat session by ID
        """
        async with async_session() as session:
            result = await session.execute(
                select(ChatSession).where(ChatSession.id == uuid.UUID(session_id))
            )
            return result.scalar_one_or_none()
    
    async def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get the chat history for a session
        """
        async with async_session() as session:
            # Join UserQuery and GeneratedResponse to get the full conversation history
            result = await session.execute(
                select(UserQuery, GeneratedResponse)
                .join(GeneratedResponse, UserQuery.id == GeneratedResponse.query_id)
                .where(UserQuery.session_id == uuid.UUID(session_id))
                .order_by(UserQuery.created_at)
            )
            
            history = []
            for user_query, generated_response in result.all():
                history.append({
                    "query": user_query.query_text,
                    "response": generated_response.response_text,
                    "timestamp": user_query.created_at,
                    "citations": generated_response.citations
                })
            
            return history
    
    async def update_session_title(self, session_id: str, new_title: str) -> bool:
        """
        Update the title of a session
        """
        async with async_session() as session:
            db_session = await self.get_session(session_id)
            if db_session:
                db_session.title = new_title
                session.add(db_session)
                await session.commit()
                return True
            return False
    
    async def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and its associated data
        """
        async with async_session() as session:
            db_session = await self.get_session(session_id)
            if db_session:
                await session.delete(db_session)
                await session.commit()
                return True
            return False


# Create a singleton instance
session_service = SessionService()