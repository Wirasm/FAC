import pytest
from app.core.config import Settings

@pytest.mark.unit
def test_settings_defaults(test_settings):
    """Test that the default settings are loaded correctly."""
    assert test_settings.APP_NAME == "FAC - FastAPI - Astro - Clerk Starter"
    assert test_settings.APP_VERSION == "0.1.0"
    assert test_settings.HOST == "127.0.0.1"
    assert test_settings.PORT == 8000
    assert test_settings.DEBUG is True

@pytest.mark.unit
def test_settings_cors_config(test_settings):
    """Test that CORS settings are configured correctly."""
    assert test_settings.CORS_ORIGINS == ["*"]
    assert test_settings.CORS_ALLOW_CREDENTIALS is False
    assert test_settings.CORS_ALLOW_METHODS == ["*"]
    assert test_settings.CORS_ALLOW_HEADERS == ["*"]
    assert test_settings.CORS_MAX_AGE == 600

@pytest.mark.unit
def test_settings_clerk_config(test_settings):
    """Test that Clerk settings are configured correctly."""
    assert test_settings.CLERK_FRONTEND_API_URL == "https://caring-bird-34.clerk.accounts.dev"
    # Secret keys might be empty in test environment
    assert hasattr(test_settings, "CLERK_SECRET_KEY")
    assert hasattr(test_settings, "CLERK_PUBLISHABLE_KEY")

@pytest.mark.unit
def test_custom_settings():
    """Test creating settings with custom values."""
    custom_settings = Settings(
        APP_NAME="Test App",
        PORT=9000,
        DEBUG=False,
        CORS_ORIGINS=["https://example.com"]
    )
    assert custom_settings.APP_NAME == "Test App"
    assert custom_settings.PORT == 9000
    assert custom_settings.DEBUG is False
    assert custom_settings.CORS_ORIGINS == ["https://example.com"]
    # Log level should be adjusted based on DEBUG
    assert custom_settings.log_level == pytest.importorskip("logging").INFO
