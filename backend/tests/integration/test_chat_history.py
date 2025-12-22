import pytest
from unittest.mock import AsyncMock, patch
from backend.src.services.session_service import SessionService


@pytest.mark.asyncio
async def test_chat_history_flow():
    """
    Integration test for chat history flow
    """
    # This would test creating a session, adding queries/responses, and retrieving history
    with patch('backend.src.config.database.async_session') as mock_session_maker:
        # Create a mock async session
        mock_session = AsyncMock()
        mock_session_maker.return_value.__aenter__.return_value = mock_session
        
        # Setup return values for queries
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None  # For get_session when session doesn't exist yet
        mock_session.execute.return_value = mock_result
        
        # Create session service instance
        session_service = SessionService()
        
        # Test creating a session
        session = await session_service.create_session(
            title="Test Session",
            metadata={"book_id": "test-book"}
        )
        
        # Verify session was created
        assert session is not None
        assert session.title == "Test Session"
        
        # In a full implementation, we would also test adding queries and retrieving history
        # For now, we're testing the basic session functionality


if __name__ == "__main__":
    pytest.main()