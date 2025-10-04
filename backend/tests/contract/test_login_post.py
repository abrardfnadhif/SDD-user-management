"""
Contract test for POST /api/login endpoint
Tests the login API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    """Test successful login with valid credentials"""
    response = await client.post(
        "/api/login",
        json={
            "email": "user@example.com",
            "password": "SecureP@ssw0rd123",
        },
    )
    
    assert response.status_code == 200
    # Check secure cookies are set
    assert "Set-Cookie" in response.headers
    cookies_header = response.headers["Set-Cookie"]
    assert "HttpOnly" in cookies_header
    assert "Secure" in cookies_header
    assert "SameSite=Strict" in cookies_header or "SameSite=strict" in cookies_header


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient) -> None:
    """Test login with invalid credentials"""
    response = await client.post(
        "/api/login",
        json={
            "email": "user@example.com",
            "password": "WrongPassword",
        },
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_login_unverified_email(client: AsyncClient) -> None:
    """Test login with unverified email"""
    response = await client.post(
        "/api/login",
        json={
            "email": "unverified@example.com",
            "password": "SecureP@ssw0rd123",
        },
    )
    
    assert response.status_code == 403
    data = response.json()
    assert "detail" in data
    assert "verif" in str(data["detail"]).lower()


@pytest.mark.asyncio
async def test_login_rate_limit(client: AsyncClient) -> None:
    """Test rate limiting after failed login attempts"""
    credentials = {
        "email": "test@example.com",
        "password": "WrongPassword",
    }
    
    # Make 5 failed attempts
    for _ in range(5):
        await client.post("/api/login", json=credentials)
    
    # 6th attempt should be rate limited
    response = await client.post("/api/login", json=credentials)
    
    assert response.status_code == 429
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_login_missing_fields(client: AsyncClient) -> None:
    """Test login with missing required fields"""
    response = await client.post(
        "/api/login",
        json={"email": "test@example.com"},
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
