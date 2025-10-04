"""
User service for user management operations
"""
from typing import Optional
import uuid
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service for user CRUD operations"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        db: AsyncSession,
        email: str,
        full_name: str,
        password: str,
        role_name: str = "User",
    ) -> User:
        """Create new user with role"""
        # Create user
        user = User(
            email=email.lower(),
            full_name=full_name,
            password_hash=UserService.hash_password(password),
            email_verified=False,
            is_active=True,
        )
        db.add(user)
        await db.flush()

        # Assign role
        role_result = await db.execute(select(Role).where(Role.name == role_name))
        role = role_result.scalar_one_or_none()

        if role:
            user_role = UserRole(user_id=user.id, role_id=role.id)
            db.add(user_role)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update_user(
        db: AsyncSession, user: User, **kwargs
    ) -> User:
        """Update user fields"""
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def schedule_deletion(
        db: AsyncSession, user: User, days: int = 30
    ) -> User:
        """Schedule user deletion"""
        user.deletion_scheduled_at = datetime.utcnow() + timedelta(days=days)
        user.is_active = False
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def cancel_deletion(db: AsyncSession, user: User) -> User:
        """Cancel scheduled deletion"""
        user.deletion_scheduled_at = None
        user.is_active = True
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user_roles(db: AsyncSession, user_id: uuid.UUID) -> list[str]:
        """Get user role names"""
        result = await db.execute(
            select(Role.name)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
        )
        return [row[0] for row in result.all()]
