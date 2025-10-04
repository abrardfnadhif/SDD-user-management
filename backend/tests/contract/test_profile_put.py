"""
Contract test for PUT /api/profile endpoint
Tests the profile update API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_update_profile_success(client: AsyncClient) -> None:
    """Test successful profile update"""
    response = await client.put(
        "/api/profile",
        json={
            "full_name": "Updated Name",
            "dob": "1990-01-01",
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert "dob" in data


@pytest.mark.asyncio
async def test_update_profile_unauthenticated(client: AsyncClient) -> None:
    """Test profile update without authentication"""
    response = await client.put(
        "/api/profile",
        json={"full_name": "Updated Name"},
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_update_profile_invalid_data(client: AsyncClient) -> None:
    """Test profile update with invalid data"""
    response = await client.put(
        "/api/profile",
        json={"full_name": ""},  # Empty name
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
