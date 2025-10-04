"""
Contract test for POST /api/2fa/verify endpoint
Tests the 2FA verification API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_2fa_verify_success(client: AsyncClient) -> None:
    """Test successful 2FA verification with valid TOTP"""
    response = await client.post(
        "/api/2fa/verify",
        json={"code": "123456"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "verified" in data
    assert data["verified"] is True


@pytest.mark.asyncio
async def test_2fa_verify_invalid_code(client: AsyncClient) -> None:
    """Test 2FA verification with invalid code"""
    response = await client.post(
        "/api/2fa/verify",
        json={"code": "000000"},
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_2fa_verify_rate_limit(client: AsyncClient) -> None:
    """Test rate limiting after failed 2FA attempts"""
    # Make 5 failed attempts
    for _ in range(5):
        await client.post("/api/2fa/verify", json={"code": "000000"})
    
    # 6th attempt should be rate limited
    response = await client.post("/api/2fa/verify", json={"code": "000000"})
    
    assert response.status_code == 429
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_2fa_verify_missing_code(client: AsyncClient) -> None:
    """Test 2FA verification without code"""
    response = await client.post("/api/2fa/verify", json={})
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
