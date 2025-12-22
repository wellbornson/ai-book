from sqlalchemy import Column, DateTime, String, Text, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func
import uuid
from backend.src.config.database import Base


class UserQuery(Base):
    """
    Represents a user's question along with context information (full-book vs selected text mode)
    """
    __tablename__ = "user_queries"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False)
    query_text = Column(Text, nullable=False)  # The actual user question
    query_mode = Column(ENUM("full-book", "selected-text", name="query_mode_enum"), nullable=False)
    selected_text = Column(Text, nullable=True)  # Optional, when in selected-text mode
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    query_metadata = Column(MutableDict.as_mutable(Text), default="{}")

    def __repr__(self):
        return f"<UserQuery(id={self.id}, session_id={self.session_id}, mode='{self.query_mode}')>"