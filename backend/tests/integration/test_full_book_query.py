import pytest
from unittest.mock import patch, MagicMock
from backend.src.services.rag_service import RAGService


@pytest.fixture
def rag_service():
    with patch('backend.src.services.embedding_service.embedding_service'), \
         patch('backend.src.services.qdrant_client.qdrant_client'), \
         patch('backend.src.services.cohere_client.cohere_client'):
        return RAGService()


def test_full_book_query_integration():
    """
    Integration test for full book query flow
    """
    # This would test the full flow: embedding query -> searching vector DB -> generating response
    # For now, we'll create a mock test since the full implementation requires external services
    
    with patch('backend.src.services.embedding_service.embedding_service') as mock_embedding, \
         patch('backend.src.services.qdrant_client.qdrant_client') as mock_qdrant, \
         patch('backend.src.services.cohere_client.cohere_client') as mock_cohere:
        
        # Setup mocks
        mock_embedding.embed_query.return_value = [0.1] * 1024  # Mock embedding
        mock_qdrant.similarity_search.return_value = [
            {
                "id": "chunk-1",
                "content": "This is a sample book content that might answer the query",
                "source_location": "Chapter 1, Page 5",
                "relevance_score": 0.85
            }
        ]
        mock_cohere.generate_response.return_value = "Based on the book content, the answer is..."
        
        # Create RAG service instance
        rag_service = RAGService()
        
        # Test the full query flow
        result = rag_service.process_query(
            query_text="What is the main theme of the book?",
            query_mode="full-book",
            session_id="test-session",
            selected_text=None
        )
        
        # Verify the result structure
        assert "response_text" in result
        assert "citations" in result
        assert len(result["citations"]) > 0
        
        # Verify that the services were called
        mock_embedding.embed_query.assert_called_once()
        mock_qdrant.similarity_search.assert_called_once()
        mock_cohere.generate_response.assert_called_once()


if __name__ == "__main__":
    pytest.main()