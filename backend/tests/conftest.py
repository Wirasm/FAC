import asyncio
import time

import jwt
import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


@pytest.fixture
def test_client():
    """
    Create a test client for the FastAPI application.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_settings():
    """
    Return the application settings for testing.
    """
    return settings

    # Create a payload similar to what Clerk would provide
    now = int(time.time())
    payload = {
        "sub": "user_test123456789",  # Subject (user ID)
        "iat": now,  # Issued at
        "exp": now + 3600,  # Expires in 1 hour
        "iss": settings.CLERK_FRONTEND_API_URL,  # Issuer
        "nbf": now - 10,  # Not valid before
        "aud": "fastapi-backend",  # Audience
        "email": "test@example.com",  # Additional claims
        "name": "Test User",
    }

    # Create header with kid that matches our test key
    headers = {"alg": "RS256", "typ": "JWT", "kid": "test_key_123"}

    # Sign the token
    token = jwt.encode(payload, algorithm="RS256", headers=headers)
    return token


@pytest.fixture
def auth_header(mock_jwt_token):
    """
    Return an Authorization header with the mock token.
    """
    return {"Authorization": f"Bearer {mock_jwt_token}"}
