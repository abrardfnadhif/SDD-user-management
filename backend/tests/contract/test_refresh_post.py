"""
Contract test for POST /api/token/refresh endpoint
Tests the token refresh API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient) -> None:
    """Test successful token refresh with valid refresh token"""
    # Assume refresh token is in cookies
    response = await client.post("/api/token/refresh")
    
    assert response.status_code == 200
    # Check new access token is set in cookies
    assert "Set-Cookie" in response.headers


@pytest.mark.asyncio
async def test_refresh_token_missing(client: AsyncClient) -> None:
    """Test token refresh without refresh token"""
    response = await client.post("/api/token/refresh")
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_refresh_token_expired(client: AsyncClient) -> None:
    """Test token refresh with expired refresh token"""
    # Set expired refresh token cookie
    response = await client.post(
        "/api/token/refresh",
        cookies={"refresh_token": "expired_token_here"},
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
