from sqlalchemy import Column, DateTime, String, Text, UUID, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func
import uuid
from backend.src.config.database import Base


class RetrievedContext(Base):
    """
    Represents the relevant book passages retrieved to answer a specific query
    """
    __tablename__ = "retrieved_contexts"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(PG_UUID(as_uuid=True), ForeignKey("user_queries.id"), nullable=False)
    content = Column(Text, nullable=False)  # The retrieved book passage
    source_location = Column(String(255), nullable=False)  # Page number, section, or other location reference
    relevance_score = Column(Float, nullable=False)  # Similarity score from vector search
    chunk_id = Column(String(255), nullable=False)  # Identifier for the specific chunk in vector DB
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    context_metadata = Column(MutableDict.as_mutable(Text), default="{}")

    def __repr__(self):
        return f"<RetrievedContext(id={self.id}, query_id={self.query_id}, score={self.relevance_score})>"