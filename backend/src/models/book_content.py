from sqlalchemy import Column, DateTime, String, Text, UUID, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func
import uuid
from backend.src.config.database import Base


class BookContent(Base):
    """
    Represents the book data that has been processed and stored in the vector database
    """
    __tablename__ = "book_contents"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    content_hash = Column(String(255), unique=True, nullable=False)  # For deduplication
    chunk_count = Column(Integer, nullable=False)  # Number of content chunks
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    book_metadata = Column(MutableDict.as_mutable(Text), default="{}")

    def __repr__(self):
        return f"<BookContent(id={self.id}, title='{self.title}', author='{self.author}')>"