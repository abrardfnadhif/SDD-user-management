"""
Contract test for POST /api/admin/users/{id}/role endpoint
Tests the admin role change API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_change_role_success(client: AsyncClient) -> None:
    """Test successful role change by admin"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.post(
        f"/api/admin/users/{user_id}/role",
        json={"role": "Admin"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "roles" in data
    assert "Admin" in data["roles"]


@pytest.mark.asyncio
async def test_admin_change_role_not_admin(client: AsyncClient) -> None:
    """Test role change by non-admin"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.post(
        f"/api/admin/users/{user_id}/role",
        json={"role": "Admin"},
    )
    
    assert response.status_code == 403
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_admin_demote_last_admin(client: AsyncClient) -> None:
    """Test demotion of last admin (should be prevented)"""
    admin_id = "last-admin-id"
    response = await client.post(
        f"/api/admin/users/{admin_id}/role",
        json={"role": "User"},
    )
    
    assert response.status_code == 409
    data = response.json()
    assert "detail" in data
    assert "last admin" in str(data["detail"]).lower()


@pytest.mark.asyncio
async def test_admin_change_role_invalid(client: AsyncClient) -> None:
    """Test role change with invalid role"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.post(
        f"/api/admin/users/{user_id}/role",
        json={"role": "InvalidRole"},
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
