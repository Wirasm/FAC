from core.config import settings
from core.logging import app_logger, setup_logger
from core.middleware import setup_cors
from fastapi import FastAPI, Depends, HTTPException, status, Request
from typing import Dict, Any
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db

from auth.clerk_deps import get_current_user, security

# Configure root logger based on settings
logging.basicConfig(level=settings.LOG_LEVEL)

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Set up CORS middleware
setup_cors(app)

app_logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.get("/api/public")
async def public_route():
    """A public endpoint that doesn't require authentication."""
    return {
        "message": "This is a public route",
        "status": "success"
    }


@app.get("/api/protected", response_model=Dict[str, Any])
async def protected_route(user: Dict[str, Any] = Depends(get_current_user)):
    """A protected endpoint that requires authentication."""
    app_logger.info(f"Protected route accessed by user: {user.get('sub')}")
    
    # Extract some basic user info for logging
    user_id = user.get('sub')
    email = user.get('email', 'unknown')
    app_logger.debug(f"User details - ID: {user_id}, Email: {email}")
    
    return {
        "message": "This is a protected route",
        "user": user,
        "authenticated": True,
        "timestamp": logging.Formatter.formatTime(logging.Formatter(), logging.LogRecord("", 0, "", 0, "", (), None))
    }


@app.get("/api/user", response_model=Dict[str, Any])
async def user_info(user: Dict[str, Any] = Depends(get_current_user)):
    """Get information about the authenticated user."""
    user_id = user.get("sub")
    app_logger.info(f"User info requested for: {user_id}")
    
    try:
        # Extract useful information from the user payload
        user_data = {
            "id": user_id,
            "email": user.get("email"),
            "name": user.get("name", ""),
            "claims": {k: v for k, v in user.items() if k not in ["sub", "email", "name"]}
        }
        
        app_logger.debug(f"User data extracted: id={user_id}, email={user_data['email']}")
        
        return {
            "message": "User information retrieved successfully",
            "user": user_data
        }
    except Exception as e:
        app_logger.error(f"Error processing user info for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing user information: {str(e)}"
        )


@app.get("/api/auth-debug")
async def auth_debug_route(request: Request):
    """Debug endpoint to check the Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    app_logger.debug(f"Authorization header: {auth_header}")
    
    if not auth_header:
        return {
            "error": "No Authorization header found",
            "help": "Add header: Authorization: Bearer YOUR_JWT_TOKEN"
        }
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return {
            "error": "Invalid Authorization header format",
            "received": auth_header,
            "expected_format": "Bearer YOUR_JWT_TOKEN",
            "help": "Make sure to include 'Bearer ' prefix before your token"
        }
    
    token = parts[1]
    return {
        "message": "Authorization header found",
        "scheme": parts[0],
        "token_length": len(token),
        "token_format": "Valid JWT format" if token.count('.') == 2 else "Invalid JWT format"
    }


@app.get("/api/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint that verifies database connectivity."""
    try:
        # Execute a simple query to check database connection
        result = await db.execute(text("SELECT 1 as is_alive"))
        is_alive = result.scalar()
        
        app_logger.debug(f"Database health check: {is_alive}")
        
        return {
            "status": "healthy",
            "database": "connected" if is_alive == 1 else "error",
            "api": "running"
        }
    except Exception as e:
        app_logger.error(f"Database health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )


@app.get("/api/debug/token")
async def debug_token(credentials = Depends(security)):
    """Debug endpoint to inspect the token (only in debug mode)."""
    if not settings.DEBUG:
        app_logger.warning("Attempt to access debug endpoint in non-debug mode")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Debug endpoints are only available in debug mode"
        )
    
    token = credentials.credentials
    app_logger.debug(f"Debug token endpoint accessed, token length: {len(token)}")
    
    # Just return the token parts without verification
    parts = token.split('.')
    if len(parts) != 3:
        app_logger.error(f"Invalid token format received: {len(parts)} parts")
        return {"error": "Invalid token format"}
    
    try:
        header = json.loads(parts[0] + '==')
        payload = json.loads(parts[1] + '==')
        
        app_logger.debug(f"Token debug - alg: {header.get('alg')}, kid: {header.get('kid')}")
        app_logger.debug(f"Token debug - sub: {payload.get('sub')}, exp: {payload.get('exp')}")
        
        return {
            "token_debug": {
                "header": header,
                "payload": payload,
                "signature": "..." # Don't show the signature
            }
        }
    except Exception as e:
        app_logger.error(f"Failed to decode token: {str(e)}")
        return {"error": f"Failed to decode token: {str(e)}"}


def main():
    """
    Entry point of the application.
    Starts the uvicorn server with the FastAPI application.
    """
    import uvicorn
    app_logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)

if __name__ == "__main__":
    main()
