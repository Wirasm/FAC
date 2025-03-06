import pytest
import time
import jwt
from fastapi.testclient import TestClient
from main import app
from core.config import settings

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

@pytest.fixture
def mock_jwt_token():
    """
    Create a mock JWT token for testing.
    
    This creates a token that looks like a valid Clerk token but is signed with a test key.
    """
    # Private key for testing (this is a test key, not a real one)
    private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj
MzEfYyjiWA4R4/M2bS1GB4t7NXp98C3SC6dVMvDuictGeurT8jNbvJZHtCSuYEvu
NMoSfm76oqFvAp8Gy0iz5sxjZmSnXyCdPEovGhLa0VzMaQ8s+CLOyS56YyCFGeJZ
agU5TzgQhQ+c3LvtQ8r+B0i1wTNZkjvBe7+W1P5j8CqrgpHtMEZGSJkj0PQFjhFX
AUHKNECnzEe5tztU0LyFgFZp1Lv4x8YmVQvp9nZVWQVXw5Nsl5gCJwJRUYhJf7Eh
48Z4xwKIYtD1ohb/JTEr0dee7D1U8MWVfs0p8jTkMBYLZgbfXA/g/QB0PA+lUHm5
Ag+RPs7XAgMBAAECggEBAKTmjaS6tkK8BlPXClTQ2vpz/N6uxDeS35mXpqasqskV
laAidgg/sWqpjXDbXr93otIMLlWsM+X0CqMDgSXKejLS2jx4GDjI1ZTXg++0AMJ8
sJ74pWzVDOfmCEQ/7wXs3+cbnXhKriO8Z036q92Qc1+N87SI38nkGa0ABH9CN83H
mQqt4fB7UdHzuIRe/me2PGhIq5ZBzj6h3BpoPGzEP+x3l9YmK8t/1cN0pqI+dQwY
dgfGjackLu/2qH80MCF7IyQaseZUOJyKrCLtSD/Iixv/hzDEUPfOCjFDgTpzf3cw
ta8+oE4wHCo1iI1/4TlPkwmXx4qSXtmw4aQPz7IDQvECgYEA8KNThCO2gsC2I9PQ
DM/8Cw0O983WCDY+oi+7JPiNAJwv5DYBqEZB1QYdj06YD16XlC/HAZMsMku1na2T
N0driwenQQWzoev3g2S7gRDoS/FCJSI3jJ+kjgtaA7Qmzlgk1TxODN+G1H91HW7t
0l7VnL27IWyYo2qRRK3jzxqUiPUCgYEAx0oQs2reBQGMVZnApD1jeq7n4MvNLcPv
t8b/eU9iUv6Y4Mj0Suo/AU8lYZXm8ubbqAlwz2VSVunD2tOplHyMUrtCtObAfVDU
AhCndKaA9gApgfb3xw1IKbuQ1u4IF1FJl3VtumfQn//LiH1B3rXhcdyo3/vIttEk
48RakUKClU8CgYEAwF6hj4L3rDqvQYrB/p8tJdrrW+B7dhgZRNkJFb0Zt3d8TI9V
11/8Y6cJk3sWDdfxrzXzLF9LVi723vW7GkEKUGJHdtsn0BjGT3lhh5XUqQDuRzSM
xZhUbnVGOqX3fPC+e9yKxzJ3dAUPKfV0I4iGzq/qwYF+S6Redwbd4GWQlkUCgYEA
qdWLx0Wd1+fxfVP5v+7EptD2bpWpqh4YfS6onoT4tIIX/kH5KtI5FTNdTX0oUUEG
2QECMi3cUAhBH8G9R8qlGLNXhpnMZnrVmjmLYI1+O9Fc9iqVaFv6qJk0h+1w8jj+
WQGdJDDwFjkhody+nGDMXAUKkEjE8rDLzNb+J+Vt8YkCgYEA7d9oPBQ+1IPLxkGy
JLqtbF5HdZRQkn+LGZBzlPv5ZwDYbYnpgzWEEL55gUZXU+NUBwRVCZCNHb661ew2
0P456RlMEIooJJZynLY0+sCHrHqVNZEKJzRYdXI+GE+M9qHh+EGLNgzFQGdJ7kBk
rCoyQ0KqNw7jELaBrKBz7yH/cX0=
-----END PRIVATE KEY-----"""
    
    # Create a payload similar to what Clerk would provide
    now = int(time.time())
    payload = {
        "sub": "user_test123456789",  # Subject (user ID)
        "iat": now,                    # Issued at
        "exp": now + 3600,             # Expires in 1 hour
        "iss": settings.CLERK_FRONTEND_API_URL,  # Issuer
        "nbf": now - 10,               # Not valid before
        "aud": "fastapi-backend",      # Audience
        "email": "test@example.com",   # Additional claims
        "name": "Test User"
    }
    
    # Create header with kid that matches our test key
    headers = {
        "alg": "RS256",
        "typ": "JWT",
        "kid": "test_key_123"
    }
    
    # Sign the token
    token = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
    return token

@pytest.fixture
def auth_header(mock_jwt_token):
    """
    Return an Authorization header with the mock token.
    """
    return {"Authorization": f"Bearer {mock_jwt_token}"}
