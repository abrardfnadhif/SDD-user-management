"""
Contract test for PUT /api/admin/users/{id} endpoint
Tests the admin user update API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_update_user_success(client: AsyncClient) -> None:
    """Test successful user update by admin"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.put(
        f"/api/admin/users/{user_id}",
        json={"full_name": "Admin Updated Name"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Admin Updated Name"


@pytest.mark.asyncio
async def test_admin_update_user_not_admin(client: AsyncClient) -> None:
    """Test user update by non-admin"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.put(
        f"/api/admin/users/{user_id}",
        json={"full_name": "Updated Name"},
    )
    
    assert response.status_code == 403
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_admin_update_user_not_found(client: AsyncClient) -> None:
    """Test user update with non-existent ID"""
    user_id = "00000000-0000-0000-0000-000000000000"
    response = await client.put(
        f"/api/admin/users/{user_id}",
        json={"full_name": "Updated Name"},
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
