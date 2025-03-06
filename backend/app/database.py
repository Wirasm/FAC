"""
Database connection and session management for the application.

This module provides utilities for connecting to the PostgreSQL database
using SQLAlchemy's async functionality, along with session management
and dependency injection for FastAPI.
"""

from typing import AsyncGenerator
import logging

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.exc import SQLAlchemyError

from core.config import settings
from core.logging import setup_logger

# Set up a database-specific logger
db_logger = setup_logger("database", settings.LOG_LEVEL)

# Create async database engine
# Format: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL = f"postgresql+asyncpg://postgres:Portlane7878@localhost:5432/playroom_db_dev"

db_logger.info(f"Initializing database connection to PostgreSQL")

# Create the SQLAlchemy engine with logging
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,  # SQL query logging
    future=True,
    pool_pre_ping=True,  # Verify connections before using them
)

# Create a session factory for creating new database sessions
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

db_logger.debug("Database engine and session factory initialized")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an async database session.
    
    Yields:
        AsyncSession: SQLAlchemy async session that will be automatically closed
                     when the request is complete.
    
    Raises:
        SQLAlchemyError: If there's an issue with the database connection or operations.
    """
    session = AsyncSessionFactory()
    db_logger.debug("Database session created")
    
    try:
        yield session
        await session.commit()
        db_logger.debug("Session committed successfully")
    except SQLAlchemyError as e:
        await session.rollback()
        db_logger.error(f"Database error occurred, session rolled back: {str(e)}")
        raise
    except Exception as e:
        await session.rollback()
        db_logger.error(f"Unexpected error occurred: {str(e)}")
        raise
    finally:
        await session.close()
        db_logger.debug("Database session closed")
