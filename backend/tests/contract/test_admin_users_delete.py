"""
Contract test for DELETE /api/admin/users/{id} endpoint
Tests the admin user deletion API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_delete_user_success(client: AsyncClient) -> None:
    """Test successful user deletion by admin"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.delete(f"/api/admin/users/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "deletion_scheduled" in data


@pytest.mark.asyncio
async def test_admin_delete_user_not_admin(client: AsyncClient) -> None:
    """Test user deletion by non-admin"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.delete(f"/api/admin/users/{user_id}")
    
    assert response.status_code == 403
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_admin_delete_last_admin(client: AsyncClient) -> None:
    """Test deletion of last admin (should be prevented)"""
    admin_id = "admin-user-id"
    response = await client.delete(f"/api/admin/users/{admin_id}")
    
    assert response.status_code == 409
    data = response.json()
    assert "detail" in data
    assert "last admin" in str(data["detail"]).lower()


@pytest.mark.asyncio
async def test_admin_delete_user_not_found(client: AsyncClient) -> None:
    """Test user deletion with non-existent ID"""
    user_id = "00000000-0000-0000-0000-000000000000"
    response = await client.delete(f"/api/admin/users/{user_id}")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
