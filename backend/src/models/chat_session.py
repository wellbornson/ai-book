from sqlalchemy import Column, DateTime, String, Text, UUID, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func
import uuid
from backend.src.config.database import Base


class ChatSession(Base):
    """
    Represents a user's conversation with the chatbot, containing metadata and history
    """
    __tablename__ = "chat_sessions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), nullable=True)  # Optional for anonymous sessions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    title = Column(String(100), nullable=False)
    session_metadata = Column(MutableDict.as_mutable(Text), default="{}")

    def __repr__(self):
        return f"<ChatSession(id={self.id}, title='{self.title}')>"