import pytest
from fastapi.testclient import TestClient
from backend.src.api.main import create_app


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def test_api_root(client):
    """
    Test the root endpoint to validate basic API functionality
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "RAG Chatbot" in response.json()["message"]


def test_api_docs_available(client):
    """
    Test that API documentation is available
    """
    response = client.get("/docs")
    assert response.status_code == 200
    assert "html" in response.text.lower()


if __name__ == "__main__":
    pytest.main()