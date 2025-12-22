import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.src.api.main import create_app


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def test_session_management_endpoints_contract(client):
    """
    Contract test for session management endpoints
    """
    # Test POST /sessions endpoint
    with patch('backend.src.api.chat_routes.verify_token') as mock_auth, \
         patch('backend.src.services.session_service.session_service') as mock_session_service:
        
        # Setup mock authentication to pass
        mock_auth.return_value = "valid-token"
        
        # Setup mock session service response
        from unittest.mock import AsyncMock
        mock_session_service.create_session = AsyncMock()
        from backend.src.models.chat_session import ChatSession
        mock_db_session = ChatSession(
            id="test-session-id",
            title="Test Session",
            created_at="2023-01-01T00:00:00"
        )
        mock_session_service.create_session.return_value = mock_db_session
        
        # Test the endpoint
        response = client.post(
            "/api/v1/sessions",
            json={
                "book_id": "test-book-id",
                "initial_context": "full-book"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Assert the response structure
        assert response.status_code == 200
        assert "session_id" in response.json()
        assert "created_at" in response.json()
        assert "book_id" in response.json()


def test_get_session_endpoint_contract(client):
    """
    Contract test for GET /sessions/{session_id} endpoint
    """
    with patch('backend.src.api.chat_routes.verify_token') as mock_auth, \
         patch('backend.src.services.session_service.session_service') as mock_session_service:
        
        # Setup mock authentication to pass
        mock_auth.return_value = "valid-token"
        
        # Setup mock session service response
        from unittest.mock import AsyncMock
        mock_session_service.get_session = AsyncMock()
        from backend.src.models.chat_session import ChatSession
        from datetime import datetime
        mock_db_session = ChatSession(
            id="test-session-id",
            user_id=None,
            title="Test Session",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={}
        )
        mock_session_service.get_session.return_value = mock_db_session
        
        # Test the endpoint
        response = client.get(
            "/api/v1/sessions/test-session-id",
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Assert the response structure
        assert response.status_code == 200
        assert "id" in response.json()
        assert "title" in response.json()
        assert "created_at" in response.json()


def test_get_session_history_endpoint_contract(client):
    """
    Contract test for GET /sessions/{session_id}/history endpoint
    """
    with patch('backend.src.api.chat_routes.verify_token') as mock_auth, \
         patch('backend.src.services.session_service.session_service') as mock_session_service:
        
        # Setup mock authentication to pass
        mock_auth.return_value = "valid-token"
        
        # Setup mock session service response
        from unittest.mock import AsyncMock
        mock_session_service.get_session_history = AsyncMock()
        mock_session_service.get_session_history.return_value = [
            {
                "query": "Test query?",
                "response": "Test response",
                "timestamp": "2023-01-01T00:00:00",
                "citations": ["Chapter 1"]
            }
        ]
        
        # Test the endpoint
        response = client.get(
            "/api/v1/sessions/test-session-id/history",
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Assert the response structure
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        if len(response.json()) > 0:
            assert "query" in response.json()[0]
            assert "response" in response.json()[0]
            assert "timestamp" in response.json()[0]


if __name__ == "__main__":
    pytest.main()