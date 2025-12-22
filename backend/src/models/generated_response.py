from sqlalchemy import Column, DateTime, Text, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func
import uuid
from backend.src.config.database import Base


class GeneratedResponse(Base):
    """
    Represents the AI-generated answer with citations to book sections
    """
    __tablename__ = "generated_responses"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(PG_UUID(as_uuid=True), ForeignKey("user_queries.id"), nullable=False)
    response_text = Column(Text, nullable=False)  # The generated response
    citations = Column(MutableDict.as_mutable(Text), default="[]")  # List of source locations referenced in response
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    response_metadata = Column(MutableDict.as_mutable(Text), default="{}")  # Generation parameters, model used, etc.

    def __repr__(self):
        return f"<GeneratedResponse(id={self.id}, query_id={self.query_id})>"