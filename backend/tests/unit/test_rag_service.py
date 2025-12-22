import pytest
from unittest.mock import patch, MagicMock
from backend.src.services.rag_service import RAGService


class TestRAGService:
    """
    Unit tests for the RAG service
    """
    
    def setup_method(self):
        self.rag_service = RAGService()
    
    @patch('backend.src.services.retrieval_service.retrieval_service')
    @patch('backend.src.services.generation_service.generation_service')
    def test_process_query_full_book_mode(self, mock_generation, mock_retrieval):
        """
        Test processing a query in full-book mode
        """
        # Setup mocks
        mock_retrieval.retrieve_relevant_context.return_value = [
            {
                "id": "chunk-1",
                "content": "This is relevant book content",
                "source_location": "Chapter 1, Page 5",
                "relevance_score": 0.85,
                "metadata": {}
            }
        ]
        
        mock_generation.generate_response.return_value = {
            "response_text": "Based on the book content, the answer is...",
            "citations": [
                {
                    "source_location": "Chapter 1, Page 5",
                    "content": "This is relevant book content"
                }
            ]
        }
        
        # Call the method
        result = self.rag_service.process_query(
            query_text="What is the main theme?",
            query_mode="full-book",
            session_id="test-session"
        )
        
        # Verify the result
        assert result["response_text"] == "Based on the book content, the answer is..."
        assert len(result["citations"]) == 1
        assert result["query_mode"] == "full-book"
        assert result["context_used"] == 1
        
        # Verify that the services were called correctly
        mock_retrieval.retrieve_relevant_context.assert_called_once()
        mock_generation.generate_response.assert_called_once()
    
    @patch('backend.src.services.retrieval_service.retrieval_service')
    @patch('backend.src.services.generation_service.generation_service')
    def test_process_query_selected_text_mode(self, mock_generation, mock_retrieval):
        """
        Test processing a query in selected-text mode
        """
        # Setup mocks
        selected_text = "This is the text the user selected."
        mock_retrieval.retrieve_relevant_context.return_value = [
            {
                "id": "selected-text",
                "content": selected_text,
                "source_location": "user-selected",
                "relevance_score": 1.0,
                "metadata": {}
            }
        ]
        
        mock_generation.generate_response.return_value = {
            "response_text": "Based on the selected text, the answer is...",
            "citations": [
                {
                    "source_location": "user-selected",
                    "content": selected_text
                }
            ]
        }
        
        # Call the method
        result = self.rag_service.process_query(
            query_text="What does this mean?",
            query_mode="selected-text",
            session_id="test-session",
            selected_text=selected_text
        )
        
        # Verify the result
        assert result["response_text"] == "Based on the selected text, the answer is..."
        assert len(result["citations"]) == 1
        assert result["query_mode"] == "selected-text"
        
        # Verify that the services were called correctly
        mock_retrieval.retrieve_relevant_context.assert_called_once()
        mock_generation.generate_response.assert_called_once()


if __name__ == "__main__":
    pytest.main()