from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.src.config.settings import settings


# Initialize the security scheme
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[str]:
    """
    Verify the authentication token
    In a real implementation, this would validate the token against an auth provider
    For now, we'll implement a simple check that can be expanded later
    """
    token = credentials.credentials

    # In a real implementation, you would validate the token against your auth provider
    # For example, with JWT: decode and verify the token
    # For now, we'll just check if it matches an expected value (this is just for demonstration)
    expected_token = settings.expected_bearer_token

    if token != expected_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token