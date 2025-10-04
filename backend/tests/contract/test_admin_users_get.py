"""
Contract test for GET /api/admin/users/{id} endpoint
Tests the admin user retrieval API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_get_user_success(client: AsyncClient) -> None:
    """Test successful user retrieval by admin"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.get(f"/api/admin/users/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "full_name" in data
    assert "roles" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_admin_get_user_not_admin(client: AsyncClient) -> None:
    """Test user retrieval by non-admin"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.get(f"/api/admin/users/{user_id}")
    
    assert response.status_code == 403
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_admin_get_user_not_found(client: AsyncClient) -> None:
    """Test user retrieval with non-existent ID"""
    user_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/api/admin/users/{user_id}")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
