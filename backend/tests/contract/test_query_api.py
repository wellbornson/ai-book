import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.src.api.main import create_app


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def test_post_query_endpoint_contract(client):
    """
    Contract test for POST /query endpoint
    """
    # Mock the necessary services to isolate the API contract test
    with patch('backend.src.api.query_routes.verify_token') as mock_auth, \
         patch('backend.src.services.rag_service.rag_service') as mock_rag:
        
        # Setup mock authentication to pass
        mock_auth.return_value = "valid-token"
        
        # Setup mock RAG service response
        mock_rag.process_query.return_value = {
            "response_id": "test-response-id",
            "response_text": "Test response",
            "citations": [
                {
                    "source_location": "Chapter 1",
                    "content": "Test content"
                }
            ],
            "query_mode": "full-book"
        }
        
        # Test the endpoint
        response = client.post(
            "/api/v1/query",
            json={
                "session_id": "test-session-id",
                "query_text": "What is the main theme?",
                "query_mode": "full-book"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Assert the response structure
        assert response.status_code == 200
        assert "response_id" in response.json()
        assert "response_text" in response.json()
        assert "citations" in response.json()
        assert "query_mode" in response.json()
        
        # Verify the query mode is as expected
        assert response.json()["query_mode"] == "full-book"


if __name__ == "__main__":
    pytest.main()