import pytest
from fastapi import status
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.mark.integration
def test_hello_world_endpoint(test_client):
    """Test the hello world endpoint."""
    response = test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}

@pytest.mark.integration
def test_public_endpoint(test_client):
    """Test the public endpoint."""
    response = test_client.get("/api/public")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "This is a public route"
    assert response.json()["status"] == "success"

@pytest.mark.integration
def test_protected_endpoint_without_auth(test_client):
    """Test that protected endpoint returns 401 or 403 without authentication."""
    response = test_client.get("/api/protected")
    # FastAPI's HTTPBearer can return either 401 or 403 depending on configuration
    assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
    assert "detail" in response.json()

@pytest.mark.integration
def test_auth_debug_endpoint_without_header(test_client):
    """Test the auth debug endpoint without an Authorization header."""
    response = test_client.get("/api/auth-debug")
    assert response.status_code == status.HTTP_200_OK
    assert "error" in response.json()
    assert response.json()["error"] == "No Authorization header found"

@pytest.mark.integration
def test_auth_debug_endpoint_with_invalid_header(test_client):
    """Test the auth debug endpoint with an invalid Authorization header."""
    response = test_client.get(
        "/api/auth-debug", 
        headers={"Authorization": "InvalidToken"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "error" in response.json()
    assert "Invalid Authorization header format" in response.json()["error"]

@pytest.mark.integration
def test_auth_debug_endpoint_with_valid_header_format(test_client):
    """Test the auth debug endpoint with a valid Authorization header format."""
    response = test_client.get(
        "/api/auth-debug", 
        headers={"Authorization": "Bearer fake.jwt.token"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    assert response.json()["token_format"] == "Valid JWT format"

@pytest.mark.integration
def test_health_check_endpoint(test_client):
    """Test the health check endpoint with a mocked database session."""
    # Create a mock for the database session
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar.return_value = 1
    mock_db.execute.return_value = mock_result
    
    # Patch the get_db dependency
    with patch('main.get_db', return_value=mock_db):
        response = test_client.get("/api/health")
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert data["api"] == "running"
        
        # Verify the database was queried
        mock_db.execute.assert_called_once()
