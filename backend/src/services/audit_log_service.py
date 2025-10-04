"""
Audit log service for tracking system actions (append-only)
"""
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.audit_log import AuditLog


class AuditLogService:
    """Service for audit logging (append-only)"""

    @staticmethod
    async def log(
        db: AsyncSession,
        action: str,
        target_type: str,
        target_id: uuid.UUID,
        actor_id: Optional[uuid.UUID] = None,
        metadata: Optional[dict] = None,
    ) -> AuditLog:
        """
        Create audit log entry (append-only)
        
        Args:
            action: Action performed (e.g., USER_CREATED, ROLE_CHANGED)
            target_type: Type of target (e.g., user, role)
            target_id: ID of target entity
            actor_id: ID of user performing action (None for system)
            metadata: Additional metadata (no raw PII)
        """
        audit_log = AuditLog(
            actor_id=actor_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            metadata=metadata or {},
            timestamp=datetime.utcnow(),
        )
        db.add(audit_log)
        await db.commit()
        await db.refresh(audit_log)
        return audit_log

    # Convenience methods for common actions

    @staticmethod
    async def log_user_created(
        db: AsyncSession,
        user_id: uuid.UUID,
        actor_id: Optional[uuid.UUID] = None,
        metadata: Optional[dict] = None,
    ) -> AuditLog:
        """Log user creation"""
        return await AuditLogService.log(
            db, "USER_CREATED", "user", user_id, actor_id, metadata
        )

    @staticmethod
    async def log_user_updated(
        db: AsyncSession,
        user_id: uuid.UUID,
        actor_id: uuid.UUID,
        fields_updated: list[str],
    ) -> AuditLog:
        """Log user profile update"""
        return await AuditLogService.log(
            db,
            "USER_UPDATED",
            "user",
            user_id,
            actor_id,
            {"fields": fields_updated},
        )

    @staticmethod
    async def log_user_deleted(
        db: AsyncSession,
        user_id: uuid.UUID,
        actor_id: uuid.UUID,
        scheduled: bool = True,
    ) -> AuditLog:
        """Log user deletion"""
        return await AuditLogService.log(
            db,
            "USER_DELETED" if not scheduled else "USER_DELETION_SCHEDULED",
            "user",
            user_id,
            actor_id,
            {"scheduled": scheduled},
        )

    @staticmethod
    async def log_login_success(
        db: AsyncSession, user_id: uuid.UUID, metadata: Optional[dict] = None
    ) -> AuditLog:
        """Log successful login"""
        return await AuditLogService.log(
            db, "LOGIN_SUCCESS", "user", user_id, user_id, metadata
        )

    @staticmethod
    async def log_login_failure(
        db: AsyncSession, email: str, metadata: Optional[dict] = None
    ) -> AuditLog:
        """Log failed login attempt"""
        # Use a dummy UUID for failed logins (no user_id available)
        dummy_id = uuid.uuid5(uuid.NAMESPACE_DNS, email)
        return await AuditLogService.log(
            db,
            "LOGIN_FAILURE",
            "user",
            dummy_id,
            None,
            {**(metadata or {}), "email": email},
        )

    @staticmethod
    async def log_role_changed(
        db: AsyncSession,
        user_id: uuid.UUID,
        actor_id: uuid.UUID,
        old_roles: list[str],
        new_roles: list[str],
    ) -> AuditLog:
        """Log role change"""
        return await AuditLogService.log(
            db,
            "ROLE_CHANGED",
            "user",
            user_id,
            actor_id,
            {"old_roles": old_roles, "new_roles": new_roles},
        )

    @staticmethod
    async def log_2fa_enabled(
        db: AsyncSession, user_id: uuid.UUID, actor_id: uuid.UUID
    ) -> AuditLog:
        """Log 2FA enablement"""
        return await AuditLogService.log(
            db, "2FA_ENABLED", "user", user_id, actor_id
        )

    @staticmethod
    async def log_2fa_disabled(
        db: AsyncSession, user_id: uuid.UUID, actor_id: uuid.UUID
    ) -> AuditLog:
        """Log 2FA disablement"""
        return await AuditLogService.log(
            db, "2FA_DISABLED", "user", user_id, actor_id
        )

    @staticmethod
    async def log_password_changed(
        db: AsyncSession, user_id: uuid.UUID, actor_id: uuid.UUID
    ) -> AuditLog:
        """Log password change"""
        return await AuditLogService.log(
            db, "PASSWORD_CHANGED", "user", user_id, actor_id
        )

    @staticmethod
    async def log_email_verified(
        db: AsyncSession, user_id: uuid.UUID
    ) -> AuditLog:
        """Log email verification"""
        return await AuditLogService.log(
            db, "EMAIL_VERIFIED", "user", user_id, user_id
        )

    @staticmethod
    async def log_access_denied(
        db: AsyncSession,
        user_id: uuid.UUID,
        resource: str,
        reason: str,
    ) -> AuditLog:
        """Log access denied (authorization failure)"""
        return await AuditLogService.log(
            db,
            "ACCESS_DENIED",
            "security",
            user_id,
            user_id,
            {"resource": resource, "reason": reason},
        )

    @staticmethod
    async def log_admin_action(
        db: AsyncSession,
        admin_id: uuid.UUID,
        action: str,
        target_id: uuid.UUID,
        metadata: Optional[dict] = None,
    ) -> AuditLog:
        """Log admin action"""
        return await AuditLogService.log(
            db,
            f"ADMIN_{action.upper()}",
            "user",
            target_id,
            admin_id,
            metadata,
        )
