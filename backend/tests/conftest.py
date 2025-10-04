"""
Pytest configuration and fixtures for all tests
"""
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """
    Async HTTP client for testing FastAPI endpoints
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
