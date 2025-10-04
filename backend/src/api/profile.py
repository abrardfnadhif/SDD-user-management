"""
Profile API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.services.user_service import UserService
from src.services.audit_log_service import AuditLogService
import uuid


router = APIRouter(prefix="/api/profile", tags=["profile"])


class ProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    dob: str | None
    two_factor_enabled: bool
    email_verified: bool
    created_at: str
    updated_at: str


class UpdateProfileRequest(BaseModel):
    full_name: str | None = None
    dob: str | None = None


@router.get("")
async def get_profile(
    user_id: str,  # TODO: Get from JWT token dependency
    db: AsyncSession = Depends(get_db),
):
    """Get user profile"""
    user = await UserService.get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "dob": user.dob.isoformat() if user.dob else None,
        "two_factor_enabled": user.two_factor_enabled,
        "email_verified": user.email_verified,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }


@router.put("")
async def update_profile(
    request: UpdateProfileRequest,
    user_id: str,  # TODO: Get from JWT token dependency
    db: AsyncSession = Depends(get_db),
):
    """Update user profile"""
    user = await UserService.get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Track updated fields
    updated_fields = []
    update_data = {}

    if request.full_name is not None:
        update_data["full_name"] = request.full_name
        updated_fields.append("full_name")

    if request.dob is not None:
        from datetime import datetime
        update_data["dob"] = datetime.fromisoformat(request.dob)
        updated_fields.append("dob")

    # Update user
    if update_data:
        user = await UserService.update_user(db, user, **update_data)

        # Log update
        await AuditLogService.log_user_updated(
            db, user.id, user.id, updated_fields
        )

    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "dob": user.dob.isoformat() if user.dob else None,
        "two_factor_enabled": user.two_factor_enabled,
        "email_verified": user.email_verified,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }
