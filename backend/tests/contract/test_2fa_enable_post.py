"""
Contract test for POST /api/2fa/enable endpoint
Tests the 2FA enrollment API contract before implementation (TDD)
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_2fa_enable_success(client: AsyncClient) -> None:
    """Test successful 2FA enrollment"""
    response = await client.post("/api/2fa/enable")
    
    assert response.status_code == 200
    data = response.json()
    assert "secret" in data
    assert "qr_code" in data
    assert "backup_codes" in data
    assert len(data["backup_codes"]) == 10


@pytest.mark.asyncio
async def test_2fa_enable_unauthenticated(client: AsyncClient) -> None:
    """Test 2FA enrollment without authentication"""
    response = await client.post("/api/2fa/enable")
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_2fa_enable_already_enabled(client: AsyncClient) -> None:
    """Test 2FA enrollment when already enabled"""
    # First enable
    await client.post("/api/2fa/enable")
    
    # Try to enable again
    response = await client.post("/api/2fa/enable")
    
    assert response.status_code == 409
    data = response.json()
    assert "detail" in data
