from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logging import app_logger


def setup_cors(app: FastAPI) -> None:
    """
    Set up CORS middleware for the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    # Get CORS settings from config
    origins = settings.CORS_ORIGINS

    # If using credentials, we can't use wildcard origins
    if settings.CORS_ALLOW_CREDENTIALS:
        # In development, use the file:// origin and localhost
        if settings.DEBUG and origins == ["*"]:
            origins = ["http://localhost:8000", "http://127.0.0.1:8000", "null"]
            app_logger.warning(
                "CORS is configured to allow specific origins in development mode with credentials."
            )
    else:
        # If not using credentials, we can use wildcard
        if settings.DEBUG or origins == ["*"]:
            origins = ["*"]
            app_logger.warning(
                "CORS is configured to allow all origins. This should not be used in production."
            )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
        expose_headers=settings.CORS_EXPOSE_HEADERS,
        max_age=settings.CORS_MAX_AGE,
    )

    app_logger.info(f"CORS middleware configured with origins: {origins}")
