"""
Contract test for POST /api/register endpoint
Tests the registration API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient) -> None:
    """Test successful user registration"""
    response = await client.post(
        "/api/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "SecureP@ssw0rd123",
            "role": "User",
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "password" not in data  # Never return password
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    """Test registration with duplicate email"""
    user_data = {
        "email": "duplicate@example.com",
        "full_name": "First User",
        "password": "SecureP@ssw0rd123",
        "role": "User",
    }
    
    # First registration
    await client.post("/api/register", json=user_data)
    
    # Duplicate registration
    response = await client.post("/api/register", json=user_data)
    
    assert response.status_code == 409
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient) -> None:
    """Test registration with invalid email format"""
    response = await client.post(
        "/api/register",
        json={
            "email": "invalid-email",
            "full_name": "Test User",
            "password": "SecureP@ssw0rd123",
            "role": "User",
        },
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient) -> None:
    """Test registration with weak password"""
    response = await client.post(
        "/api/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "weak",
            "role": "User",
        },
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "password" in str(data["detail"]).lower()


@pytest.mark.asyncio
async def test_register_missing_fields(client: AsyncClient) -> None:
    """Test registration with missing required fields"""
    response = await client.post(
        "/api/register",
        json={"email": "test@example.com"},
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
