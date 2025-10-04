"""
Contract test for GET /api/profile endpoint
Tests the profile retrieval API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_profile_success(client: AsyncClient) -> None:
    """Test successful profile retrieval"""
    response = await client.get("/api/profile")
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "full_name" in data
    assert "two_factor_enabled" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_get_profile_unauthenticated(client: AsyncClient) -> None:
    """Test profile retrieval without authentication"""
    response = await client.get("/api/profile")
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
