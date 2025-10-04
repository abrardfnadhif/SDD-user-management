"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.services.mfa_service import MFAService
from src.services.audit_log_service import AuditLogService


router = APIRouter(prefix="/api", tags=["auth"])


# Request/Response models
class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str = "User"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Verify2FARequest(BaseModel):
    code: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    two_factor_enabled: bool
    email_verified: bool
    created_at: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register new user"""
    # Check if user exists
    existing = await UserService.get_user_by_email(db, request.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create user
    user = await UserService.create_user(
        db, request.email, request.full_name, request.password, request.role
    )

    # Log user creation
    await AuditLogService.log_user_created(db, user.id)

    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "two_factor_enabled": user.two_factor_enabled,
        "email_verified": user.email_verified,
        "created_at": user.created_at.isoformat(),
    }


@router.post("/login")
async def login(
    request: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Login with email and password"""
    # Authenticate user
    user = await AuthService.authenticate_user(db, request.email, request.password)
    
    if not user:
        # Log failed login
        await AuditLogService.log_login_failure(db, request.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Check email verification
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified",
        )

    # Create tokens
    tokens = AuthService.create_token_pair(user)

    # Set secure cookies
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=900,  # 15 minutes
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=604800,  # 7 days
    )

    # Log successful login
    await AuditLogService.log_login_success(db, user.id)

    return {"message": "Login successful", "requires_2fa": user.two_factor_enabled}


@router.post("/token/refresh")
async def refresh_token(
    response: Response,
    refresh_token: str = None,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token"""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required",
        )

    # Refresh access token
    result = await AuthService.refresh_access_token(db, refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Set new access token cookie
    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=900,
    )

    return {"message": "Token refreshed"}


@router.post("/2fa/enable")
async def enable_2fa(
    user_id: str,  # TODO: Get from JWT token
    db: AsyncSession = Depends(get_db),
):
    """Enable 2FA for user"""
    import uuid
    user = await UserService.get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="2FA already enabled",
        )

    # Enable 2FA
    result = await MFAService.enable_2fa(db, user)

    # Log 2FA enablement
    await AuditLogService.log_2fa_enabled(db, user.id, user.id)

    return result


@router.post("/2fa/verify")
async def verify_2fa(
    request: Verify2FARequest,
    user_id: str,  # TODO: Get from JWT token
    db: AsyncSession = Depends(get_db),
):
    """Verify 2FA code"""
    import uuid
    user = await UserService.get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Verify code
    valid = await MFAService.verify_2fa_code(db, user, request.code)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid 2FA code",
        )

    return {"verified": True}
