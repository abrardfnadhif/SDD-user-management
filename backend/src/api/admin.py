"""
Admin API endpoints with RBAC enforcement
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.services.user_service import UserService
from src.services.rbac_service import RBACService
from src.services.audit_log_service import AuditLogService
import uuid


router = APIRouter(prefix="/api/admin/users", tags=["admin"])


class UpdateUserRequest(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None


class ChangeRoleRequest(BaseModel):
    role: str


async def verify_admin(admin_id: str, db: AsyncSession) -> None:
    """Verify user is admin (helper function)"""
    is_admin = await RBACService.is_admin(db, uuid.UUID(admin_id))
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    admin_id: str,  # TODO: Get from JWT token
    db: AsyncSession = Depends(get_db),
):
    """Get user by ID (admin only)"""
    await verify_admin(admin_id, db)

    user = await UserService.get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Get user roles
    roles = await RBACService.get_user_roles(db, user.id)

    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "roles": roles,
        "two_factor_enabled": user.two_factor_enabled,
        "email_verified": user.email_verified,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    admin_id: str,  # TODO: Get from JWT token
    db: AsyncSession = Depends(get_db),
):
    """Update user (admin only)"""
    await verify_admin(admin_id, db)

    user = await UserService.get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Update user
    update_data = {}
    if request.full_name is not None:
        update_data["full_name"] = request.full_name
    if request.is_active is not None:
        update_data["is_active"] = request.is_active

    if update_data:
        user = await UserService.update_user(db, user, **update_data)

        # Log admin action
        await AuditLogService.log_admin_action(
            db, uuid.UUID(admin_id), "UPDATE_USER", user.id, update_data
        )

    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
    }


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    admin_id: str,  # TODO: Get from JWT token
    db: AsyncSession = Depends(get_db),
):
    """Delete user (admin only) - T040: Enforce last-admin rule"""
    await verify_admin(admin_id, db)

    user = await UserService.get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # T040: Check last-admin rule
    can_delete, reason = await RBACService.can_delete_user(db, user.id)
    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=reason,
        )

    # Schedule deletion (30 days)
    user = await UserService.schedule_deletion(db, user, days=30)

    # Log deletion
    await AuditLogService.log_user_deleted(
        db, user.id, uuid.UUID(admin_id), scheduled=True
    )

    return {
        "message": "User deletion scheduled",
        "deletion_scheduled": True,
        "deletion_scheduled_at": user.deletion_scheduled_at.isoformat(),
    }


@router.post("/{user_id}/role")
async def change_user_role(
    user_id: str,
    request: ChangeRoleRequest,
    admin_id: str,  # TODO: Get from JWT token
    db: AsyncSession = Depends(get_db),
):
    """Change user role (admin only) - T040: Enforce last-admin rule"""
    await verify_admin(admin_id, db)

    user = await UserService.get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Get current roles
    old_roles = await RBACService.get_user_roles(db, user.id)

    # T040: Change role with last-admin protection
    success, message = await RBACService.change_role(
        db, user.id, request.role
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )

    # Get new roles
    new_roles = await RBACService.get_user_roles(db, user.id)

    # Log role change
    await AuditLogService.log_role_changed(
        db, user.id, uuid.UUID(admin_id), old_roles, new_roles
    )

    return {
        "id": str(user.id),
        "roles": new_roles,
        "message": message,
    }


@router.post("/{user_id}/cancel-deletion")
async def cancel_deletion(
    user_id: str,
    admin_id: str,  # TODO: Get from JWT token
    db: AsyncSession = Depends(get_db),
):
    """Cancel scheduled deletion (admin only) - T041: 14-day cancellation window"""
    await verify_admin(admin_id, db)

    user = await UserService.get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.deletion_scheduled_at:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No deletion scheduled for this user",
        )

    # Check if within 14-day cancellation window
    from datetime import datetime, timedelta
    scheduled_date = user.deletion_scheduled_at
    cancellation_deadline = scheduled_date + timedelta(days=14)
    
    if datetime.utcnow() > cancellation_deadline:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cancellation window (14 days) has expired",
        )

    # Cancel deletion
    user = await UserService.cancel_deletion(db, user)

    # Log cancellation
    await AuditLogService.log_admin_action(
        db, uuid.UUID(admin_id), "CANCEL_DELETION", user.id
    )

    return {
        "message": "Deletion cancelled",
        "deletion_cancelled": True,
    }
