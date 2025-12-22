"""
Database models for the RAG Chatbot for Published Book
"""
from backend.src.config.database import Base
from backend.src.models.chat_session import ChatSession
from backend.src.models.book_content import BookContent
from backend.src.models.user_query import UserQuery
from backend.src.models.retrieved_context import RetrievedContext
from backend.src.models.generated_response import GeneratedResponse


# Import all models to ensure they are registered with SQLAlchemy
__all__ = [
    "Base",
    "ChatSession",
    "BookContent", 
    "UserQuery",
    "RetrievedContext",
    "GeneratedResponse"
]