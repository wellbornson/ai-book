from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from backend.src.config.settings import settings
import uuid


class QdrantDBClient:
    """
    Qdrant vector database client wrapper
    """

    def __init__(self):
        # Use in-memory Qdrant for development if no URL is provided
        if not settings.qdrant_url or settings.qdrant_url == "your_qdrant_url_here":
            # Use in-memory mode for development
            self.client = QdrantClient(":memory:")
            print("Using in-memory Qdrant for development")
        else:
            # Initialize Qdrant client with cloud configuration
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False  # Using HTTP for cloud instance
            )
            print(f"Using Qdrant at {settings.qdrant_url}")

        # Collection name for book content
        self.collection_name = "book_content_chunks"

        # Create collection if it doesn't exist
        self._create_collection()
        
    def _create_collection(self):
        """
        Create the collection for storing book content chunks with 1024-dim vectors and Cosine similarity
        """
        try:
            # Check if collection already exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection with 1024-dim vectors and Cosine similarity as specified
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # 1024-dim vectors as specified
                    distance=models.Distance.COSINE  # Cosine similarity as specified
                )
            )
            
            print(f"Created collection '{self.collection_name}' with 1024-dim vectors and Cosine similarity")
    
    def add_texts(
        self, 
        texts: List[str], 
        metadatas: List[Dict[str, Any]] = None, 
        ids: List[str] = None
    ) -> List[str]:
        """
        Add texts to the vector store
        """
        import uuid
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        
        # Create embeddings for the texts
        # This would typically be done with an embedding service
        # For now, we'll represent the process
        
        # Prepare points for insertion
        points = []
        for i, text in enumerate(texts):
            payload = {
                "content": text,
                "metadata": metadatas[i] if metadatas else {}
            }
            
            # In a real implementation, you would generate actual embeddings here
            # For now, we'll just note that this is where embedding would happen
            points.append(
                models.PointStruct(
                    id=ids[i],
                    vector=[0.0] * 1024,  # Placeholder - in real implementation, this would be actual embedding
                    payload=payload
                )
            )
        
        # Upload points to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return ids
    
    def similarity_search(
        self, 
        query_embedding: List[float], 
        k: int = 4,
        filter: Optional[models.Filter] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search in the vector store
        """
        # Search for similar vectors
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k,
            query_filter=filter
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "content": result.payload["content"],
                "source_location": result.payload["metadata"].get("source_location", ""),
                "relevance_score": result.score,
                "metadata": result.payload["metadata"]
            })
        
        return formatted_results
    
    def delete_collection(self):
        """
        Delete the collection (useful for testing/refreshing)
        """
        self.client.delete_collection(self.collection_name)
    
    def get_collection_info(self):
        """
        Get information about the collection
        """
        return self.client.get_collection(self.collection_name)


# Create a singleton instance
qdrant_client = QdrantDBClient()