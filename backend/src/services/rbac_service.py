"""
RBAC (Role-Based Access Control) service for authorization
"""
from typing import Optional
import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole


class RBACService:
    """Service for role-based access control"""

    @staticmethod
    async def has_role(db: AsyncSession, user_id: uuid.UUID, role_name: str) -> bool:
        """Check if user has specific role"""
        result = await db.execute(
            select(UserRole)
            .join(Role, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id, Role.name == role_name)
        )
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def is_admin(db: AsyncSession, user_id: uuid.UUID) -> bool:
        """Check if user is admin"""
        return await RBACService.has_role(db, user_id, "Admin")

    @staticmethod
    async def get_user_roles(db: AsyncSession, user_id: uuid.UUID) -> list[str]:
        """Get all role names for user"""
        result = await db.execute(
            select(Role.name)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
        )
        return [row[0] for row in result.all()]

    @staticmethod
    async def assign_role(
        db: AsyncSession, user_id: uuid.UUID, role_name: str
    ) -> bool:
        """Assign role to user"""
        # Get role
        role_result = await db.execute(select(Role).where(Role.name == role_name))
        role = role_result.scalar_one_or_none()
        if not role:
            return False

        # Check if already assigned
        existing = await db.execute(
            select(UserRole).where(
                UserRole.user_id == user_id, UserRole.role_id == role.id
            )
        )
        if existing.scalar_one_or_none():
            return True  # Already assigned

        # Assign role
        user_role = UserRole(user_id=user_id, role_id=role.id)
        db.add(user_role)
        await db.commit()
        return True

    @staticmethod
    async def remove_role(
        db: AsyncSession, user_id: uuid.UUID, role_name: str
    ) -> bool:
        """Remove role from user"""
        # Get role
        role_result = await db.execute(select(Role).where(Role.name == role_name))
        role = role_result.scalar_one_or_none()
        if not role:
            return False

        # Find and delete user_role
        result = await db.execute(
            select(UserRole).where(
                UserRole.user_id == user_id, UserRole.role_id == role.id
            )
        )
        user_role = result.scalar_one_or_none()
        if user_role:
            await db.delete(user_role)
            await db.commit()
            return True

        return False

    @staticmethod
    async def count_admins(db: AsyncSession) -> int:
        """Count total number of active admins"""
        result = await db.execute(
            select(func.count(UserRole.user_id))
            .join(Role, UserRole.role_id == Role.id)
            .join(User, UserRole.user_id == User.id)
            .where(Role.name == "Admin", User.is_active == True)
        )
        return result.scalar_one()

    @staticmethod
    async def is_last_admin(db: AsyncSession, user_id: uuid.UUID) -> bool:
        """
        Check if user is the last active admin
        
        Used to prevent orphaned admin situation
        """
        # Check if user is admin
        if not await RBACService.is_admin(db, user_id):
            return False

        # Count total admins
        admin_count = await RBACService.count_admins(db)
        return admin_count == 1

    @staticmethod
    async def can_delete_user(db: AsyncSession, user_id: uuid.UUID) -> tuple[bool, str]:
        """
        Check if user can be deleted
        
        Returns:
            (can_delete, reason)
        """
        # Check if last admin
        if await RBACService.is_last_admin(db, user_id):
            return False, "Cannot delete the last active admin"

        return True, ""

    @staticmethod
    async def can_demote_user(
        db: AsyncSession, user_id: uuid.UUID, from_role: str
    ) -> tuple[bool, str]:
        """
        Check if user can be demoted from a role
        
        Returns:
            (can_demote, reason)
        """
        # If demoting from Admin, check if last admin
        if from_role == "Admin" and await RBACService.is_last_admin(db, user_id):
            return False, "Cannot demote the last active admin"

        return True, ""

    @staticmethod
    async def change_role(
        db: AsyncSession, user_id: uuid.UUID, new_role_name: str
    ) -> tuple[bool, str]:
        """
        Change user's role (remove all roles and assign new one)
        
        Returns:
            (success, message)
        """
        # Get current roles
        current_roles = await RBACService.get_user_roles(db, user_id)

        # Check if can demote from Admin
        if "Admin" in current_roles and new_role_name != "Admin":
            can_demote, reason = await RBACService.can_demote_user(db, user_id, "Admin")
            if not can_demote:
                return False, reason

        # Remove all current roles
        for role_name in current_roles:
            await RBACService.remove_role(db, user_id, role_name)

        # Assign new role
        success = await RBACService.assign_role(db, user_id, new_role_name)
        if success:
            return True, f"Role changed to {new_role_name}"
        else:
            return False, f"Role {new_role_name} not found"
