# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def async_client():
    """Provides an isolated asynchronous HTTP client for testing."""
    # Using ASGITransport links HTTPX directly to your FastAPI app without starting a real server
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client