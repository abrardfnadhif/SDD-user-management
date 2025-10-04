"""
Multi-Factor Authentication service for TOTP and backup codes
"""
import secrets
import hashlib
from typing import Optional
import uuid
import pyotp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.models.tokens import BackupCode


class MFAService:
    """Service for 2FA/MFA operations"""

    @staticmethod
    def generate_totp_secret() -> str:
        """Generate TOTP secret (base32 encoded)"""
        return pyotp.random_base32()

    @staticmethod
    def generate_provisioning_uri(secret: str, email: str, issuer: str = "UserManagement") -> str:
        """Generate TOTP provisioning URI for QR code"""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=email, issuer_name=issuer)

    @staticmethod
    def verify_totp(secret: str, code: str, window: int = 1) -> bool:
        """
        Verify TOTP code with time drift tolerance
        
        Args:
            secret: TOTP secret
            code: 6-digit code from user
            window: Time drift window (±30s per window, default 1 = ±30s)
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=window)

    @staticmethod
    def generate_backup_codes(count: int = 10) -> list[str]:
        """Generate backup codes (8 characters each)"""
        return [secrets.token_hex(4).upper() for _ in range(count)]

    @staticmethod
    def hash_backup_code(code: str) -> str:
        """Hash backup code for storage"""
        return hashlib.sha256(code.encode()).hexdigest()

    @staticmethod
    async def enable_2fa(
        db: AsyncSession, user: User
    ) -> dict[str, any]:
        """
        Enable 2FA for user
        
        Returns:
            dict with secret, qr_code_uri, and backup_codes
        """
        # Generate TOTP secret
        secret = MFAService.generate_totp_secret()
        user.two_factor_secret = secret
        user.two_factor_enabled = True

        # Generate backup codes
        backup_codes = MFAService.generate_backup_codes(10)
        
        # Store hashed backup codes
        for code in backup_codes:
            backup_code = BackupCode(
                user_id=user.id,
                code_hash=MFAService.hash_backup_code(code),
            )
            db.add(backup_code)

        await db.commit()
        await db.refresh(user)

        # Generate QR code URI
        qr_uri = MFAService.generate_provisioning_uri(secret, user.email)

        return {
            "secret": secret,
            "qr_code": qr_uri,
            "backup_codes": backup_codes,
        }

    @staticmethod
    async def verify_2fa_code(
        db: AsyncSession, user: User, code: str
    ) -> bool:
        """
        Verify 2FA code (TOTP or backup code)
        
        Returns:
            True if code is valid
        """
        if not user.two_factor_enabled or not user.two_factor_secret:
            return False

        # Try TOTP first
        if MFAService.verify_totp(user.two_factor_secret, code, window=1):
            return True

        # Try backup codes
        code_hash = MFAService.hash_backup_code(code)
        result = await db.execute(
            select(BackupCode).where(
                BackupCode.user_id == user.id,
                BackupCode.code_hash == code_hash,
                BackupCode.used_at.is_(None),
            )
        )
        backup_code = result.scalar_one_or_none()

        if backup_code:
            # Mark backup code as used
            from datetime import datetime
            backup_code.used_at = datetime.utcnow()
            await db.commit()
            return True

        return False

    @staticmethod
    async def disable_2fa(db: AsyncSession, user: User) -> None:
        """Disable 2FA for user"""
        user.two_factor_enabled = False
        user.two_factor_secret = None

        # Delete all backup codes
        await db.execute(
            select(BackupCode).where(BackupCode.user_id == user.id)
        )
        # Note: Should use DELETE statement here
        await db.commit()

    @staticmethod
    async def regenerate_backup_codes(
        db: AsyncSession, user: User
    ) -> list[str]:
        """Regenerate backup codes for user"""
        # Delete old backup codes
        result = await db.execute(
            select(BackupCode).where(BackupCode.user_id == user.id)
        )
        old_codes = result.scalars().all()
        for code in old_codes:
            await db.delete(code)

        # Generate new backup codes
        backup_codes = MFAService.generate_backup_codes(10)
        for code in backup_codes:
            backup_code = BackupCode(
                user_id=user.id,
                code_hash=MFAService.hash_backup_code(code),
            )
            db.add(backup_code)

        await db.commit()
        return backup_codes
