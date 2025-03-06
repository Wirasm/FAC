from typing import Any, Dict, Optional

import requests
from core.config import settings
from core.logging import auth_logger
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwk, jwt

# Initialize security scheme
# When auto_error=True, it returns 403 Forbidden when no token is provided
# We'll handle the 401 Unauthorized in our dependency function
security = HTTPBearer(auto_error=True)


def get_clerk_jwt_public_key(token: str):
    """
    Fetch the Clerk JWT public key from the JWKS endpoint based on the token's key ID.

    Args:
        token (str): The JWT token

    Returns:
        str: The PEM-encoded public key

    Raises:
        HTTPException: If the key cannot be retrieved or is invalid
    """
    try:
        # Get the kid (key ID) from the token headers
        headers = jwt.get_unverified_headers(token)
        kid = headers.get("kid")

        auth_logger.debug(f"Token kid: {kid}")

        if not kid:
            auth_logger.error("No 'kid' found in token headers")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: No key ID (kid) found in token headers",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Fetch the JWKS from Clerk
        jwks_url = f"{settings.CLERK_FRONTEND_API_URL}/.well-known/jwks.json"
        auth_logger.debug(f"Fetching JWKS from: {jwks_url}")

        try:
            response = requests.get(jwks_url, timeout=5)  # Add timeout
            response.raise_for_status()
        except requests.RequestException as e:
            auth_logger.error(f"Failed to fetch JWKS from {jwks_url}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to verify authentication: JWKS endpoint unreachable",
                headers={"WWW-Authenticate": "Bearer"},
            )

        jwks = response.json()

        # Find the key that matches the kid
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                auth_logger.debug(f"Found matching key for kid: {kid}")
                return jwk.construct(key).to_pem().decode("utf-8")

        auth_logger.error(f"No key found with kid: {kid}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: No matching key found for key ID (kid): {kid}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        # Pass through HTTPExceptions we've already created
        raise
    except Exception as e:
        # Convert other unexpected exceptions to HTTPException
        auth_logger.exception(f"Unexpected error getting public key: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error during token verification",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify the JWT token from Clerk.
    """
    try:
        auth_logger.debug("Starting token verification")

        # Get basic token info for logging
        headers = jwt.get_unverified_headers(token)
        auth_logger.debug(
            f"Token headers: alg={headers.get('alg')}, typ={headers.get('typ')}"
        )

        # Get the public key using the token's key ID
        public_key = get_clerk_jwt_public_key(token)
        auth_logger.debug("Public key retrieved successfully")

        # Decode and verify the token
        auth_logger.debug(
            f"Decoding token with public key (audience='fastapi-backend', issuer='{settings.CLERK_FRONTEND_API_URL}')"
        )
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="fastapi-backend",  # Make sure this matches your JWT template
            issuer=settings.CLERK_FRONTEND_API_URL,
            options={"verify_signature": True},
        )

        # Log successful verification with user details
        user_id = payload.get("sub")
        auth_logger.info(f"Token verified successfully for user: {user_id}")

        # Log additional useful information about the token
        auth_logger.debug(
            f"Token issued at: {payload.get('iat')}, expires: {payload.get('exp')}"
        )
        auth_logger.debug(f"Token contains {len(payload)} claims")

        return payload
    except JWTError as e:
        auth_logger.error(f"Token verification failed: {str(e)}")
        # Log more details about the failure
        auth_logger.debug(f"Token verification error details: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """
    Get the current authenticated user from the token.

    Args:
        credentials (HTTPAuthorizationCredentials): The credentials from the request

    Returns:
        Dict[str, Any]: The user information from the token

    Raises:
        HTTPException: If authentication fails
    """
    auth_logger.debug("Getting current user from credentials")
    token = credentials.credentials

    # Log token details for debugging
    auth_logger.debug(f"Token received, length: {len(token)}")
    auth_logger.debug(f"Token starts with: {token[:20]}...")

    # Check if token looks like a JWT (should have 2 dots)
    if token.count(".") != 2:
        auth_logger.error(
            f"Invalid token format: expected JWT with 2 dots, got {token.count('.')} dots"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format. Expected JWT token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_token(token)

    user_id = payload.get("sub")
    auth_logger.info(f"User authenticated: {user_id}")

    return payload
