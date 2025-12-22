import pytest
from unittest.mock import patch
from backend.src.services.rag_service import RAGService


def test_selected_text_query_integration():
    """
    Integration test for user-selected text query flow
    """
    # This would test the flow when query_mode is "selected-text"
    with patch('backend.src.services.embedding_service.embedding_service'), \
         patch('backend.src.services.qdrant_client.qdrant_client'), \
         patch('backend.src.services.cohere_client.cohere_client') as mock_cohere:
        
        # Setup mock for Cohere to return a response
        mock_cohere.generate_response.return_value = "Based on the selected text, the answer is..."
        
        # Create RAG service instance
        rag_service = RAGService()
        
        # Test the selected text query flow
        result = rag_service.process_query(
            query_text="What does this selected text mean?",
            query_mode="selected-text",
            session_id="test-session",
            selected_text="This is the specific text the user selected from the book."
        )
        
        # Verify the result structure
        assert "response_text" in result
        assert "citations" in result
        assert result["query_mode"] == "selected-text"
        
        # For selected-text mode, the response should be based on the provided text
        # rather than searching in the vector DB


if __name__ == "__main__":
    pytest.main()