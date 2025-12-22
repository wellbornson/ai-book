from typing import List, Dict, Any
from backend.src.services.qdrant_client import qdrant_client
from backend.src.services.embedding_service import embedding_service
from backend.src.utils.error_handler import QueryProcessingError


class RetrievalService:
    """
    Service for retrieving relevant book content based on user queries
    """

    def __init__(self):
        pass

    def retrieve_relevant_context(
        self,
        query: str,
        top_k: int = 4,
        query_mode: str = "full-book",
        selected_text: str = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context based on the query
        """
        if query_mode == "selected-text":
            if not selected_text:
                raise QueryProcessingError("Selected text is required for selected-text mode")

            # If in selected-text mode, return the selected text as context
            return [{
                "id": "selected-text",
                "content": selected_text,
                "source_location": "user-selected",
                "relevance_score": 1.0,
                "metadata": {}
            }]
        elif query_mode == "full-book":
            # For full-book mode, search in the vector database
            query_embedding = embedding_service.embed_query(query)
            results = qdrant_client.similarity_search(
                query_embedding=query_embedding,
                k=top_k
            )
            return results
        else:
            raise QueryProcessingError(f"Invalid query mode: {query_mode}")


# Create a singleton instance
retrieval_service = RetrievalService()