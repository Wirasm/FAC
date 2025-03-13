"""
Tests for the database connection and session management.

This module contains tests for the database.py functionality,
including connection setup, session management, and dependency injection.
"""

from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionFactory, engine, get_db


@pytest.mark.unit
@pytest.mark.asyncio
async def test_engine_creation():
    """Test that the database engine is created correctly."""
    assert engine is not None
    assert engine.dialect.name == "postgresql"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_session_factory():
    """Test that the session factory creates sessions correctly."""
    # Just test that the factory creates a session of the right type
    # without trying to use async operations that require greenlet
    session = AsyncSessionFactory()
    assert isinstance(session, AsyncSession)
    # Don't call await session.close() as it requires greenlet


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_db_success():
    """Test the get_db dependency with successful operations."""
    # Create a mock session
    mock_session = AsyncMock(spec=AsyncSession)

    # Patch the AsyncSessionFactory to return our mock
    with patch("app.database.AsyncSessionFactory", return_value=mock_session):
        # Use the get_db dependency
        db_gen = get_db()
        session = await anext(db_gen)

        # Verify we got our mock session
        assert session is mock_session

        # Complete the generator
        try:
            await db_gen.__anext__()
        except StopAsyncIteration:
            pass

        # Verify session operations were called
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()
        mock_session.rollback.assert_not_called()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_db_sqlalchemy_error():
    """Test the get_db dependency with a SQLAlchemy error."""
    # Create a mock session
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.commit.side_effect = SQLAlchemyError("Database error")

    # Patch the AsyncSessionFactory to return our mock
    with patch("app.database.AsyncSessionFactory", return_value=mock_session):
        # Use the get_db dependency
        db_gen = get_db()
        session = await anext(db_gen)

        # Verify we got our mock session
        assert session is mock_session

        # Complete the generator, expecting an error
        with pytest.raises(SQLAlchemyError, match="Database error"):
            await db_gen.__anext__()

        # Verify session operations were called
        mock_session.commit.assert_called_once()
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_db_general_exception():
    """Test the get_db dependency with a general exception."""
    # Create a mock session
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.commit.side_effect = ValueError("Some other error")

    # Patch the AsyncSessionFactory to return our mock
    with patch("app.database.AsyncSessionFactory", return_value=mock_session):
        # Use the get_db dependency
        db_gen = get_db()
        session = await anext(db_gen)

        # Verify we got our mock session
        assert session is mock_session

        # Complete the generator, expecting an error
        with pytest.raises(ValueError, match="Some other error"):
            await db_gen.__anext__()

        # Verify session operations were called
        mock_session.commit.assert_called_once()
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_database_connection():
    """
    Test connecting to the actual database.

    This test requires a running database instance.
    """
    # Create a new connection with the current event loop
    # The session factory will use the default event loop automatically
    async with AsyncSessionFactory() as session:
        from sqlalchemy import text

        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
