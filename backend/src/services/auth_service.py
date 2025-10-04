"""
Authentication service for JWT and session management
"""
from datetime import datetime, timedelta
from typing import Optional
import uuid
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.services.user_service import UserService


# JWT Configuration (should come from settings)
SECRET_KEY = "your-secret-key-change-in-production"  # TODO: Move to settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


class AuthService:
    """Service for authentication and JWT management"""

    @staticmethod
    def create_access_token(
        user_id: uuid.UUID, email: str, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "type": "access",
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def create_refresh_token(user_id: uuid.UUID, email: str) -> str:
        """Create JWT refresh token"""
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != token_type:
                return None
            return payload
        except JWTError:
            return None

    @staticmethod
    async def authenticate_user(
        db: AsyncSession, email: str, password: str
    ) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not UserService.verify_password(password, user.password_hash):
            return None
        if not user.is_active:
            return None
        return user

    @staticmethod
    def create_token_pair(user: User) -> dict[str, str]:
        """Create access and refresh token pair"""
        access_token = AuthService.create_access_token(user.id, user.email)
        refresh_token = AuthService.create_refresh_token(user.id, user.email)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    async def refresh_access_token(
        db: AsyncSession, refresh_token: str
    ) -> Optional[dict[str, str]]:
        """Refresh access token using refresh token"""
        payload = AuthService.verify_token(refresh_token, "refresh")
        if not payload:
            return None

        user_id = uuid.UUID(payload["sub"])
        user = await UserService.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            return None

        # Create new access token
        access_token = AuthService.create_access_token(user.id, user.email)
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    @staticmethod
    async def revoke_all_sessions(db: AsyncSession, user: User) -> None:
        """
        Revoke all user sessions
        
        Note: With stateless JWT, this requires:
        1. Token blacklist (not implemented yet)
        2. Or changing user's secret/salt
        3. Or tracking token versions
        
        For now, this is a placeholder for future implementation
        """
        # TODO: Implement token blacklist or version tracking
        pass
