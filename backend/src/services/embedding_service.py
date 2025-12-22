from typing import List
from backend.src.services.cohere_client import cohere_client


class EmbeddingService:
    """
    Service for creating embeddings using Cohere API
    """
    
    def __init__(self):
        pass
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for documents with proper input_type specification
        """
        return cohere_client.embed_documents(texts)
    
    def embed_query(self, query: str) -> List[float]:
        """
        Create embeddings for a query with proper input_type specification
        """
        return cohere_client.embed_query(query)


# Create a singleton instance
embedding_service = EmbeddingService()