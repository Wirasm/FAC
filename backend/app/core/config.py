import logging
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # App info
    APP_NAME: str = "FAC - FastAPI - Astro - Clerk Starter"
    APP_DESCRIPTION: str = "A full-stack starter template integrating FastAPI backend with Astro frontend and Clerk authentication"
    APP_VERSION: str = "0.1.0"

    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Add more settings as needed
    DEBUG: bool = True

    # Logging settings
    LOG_LEVEL: int = logging.DEBUG if DEBUG else logging.INFO

    @property
    def log_level(self) -> int:
        """Dynamic property that returns the appropriate log level based on DEBUG setting."""
        return logging.DEBUG if self.DEBUG else logging.INFO

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]  # Allow all origins in development
    CORS_ALLOW_CREDENTIALS: bool = False  # Set to False to allow wildcard origin
    CORS_ALLOW_METHODS: List[str] = ["*"]  # Allow all methods
    CORS_ALLOW_HEADERS: List[str] = ["*"]  # Allow all headers
    CORS_EXPOSE_HEADERS: List[str] = []
    CORS_MAX_AGE: int = 600  # 10 minutes

    # Database settings
    DATABASE_URL: str = "postgresql://postgres:yourpassword@localhost/items-db-dev"
    
    # Clerk Authentication Settings
    CLERK_SECRET_KEY: str = ""
    CLERK_PUBLISHABLE_KEY: str = ""
    CLERK_FRONTEND_API_URL: str = "https://caring-bird-34.clerk.accounts.dev"

    class ConfigDict:
        env_file = ".env"
        case_sensitive = True


# Create a global settings object
settings = Settings()
