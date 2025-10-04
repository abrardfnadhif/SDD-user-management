"""
Role model
"""
import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.session import Base


class Role(Base):
    """Role model for RBAC"""

    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)

    # Relationships
    user_roles: Mapped[list["UserRole"]] = relationship("UserRole", back_populates="role")

    def __repr__(self) -> str:
        return f"<Role {self.name}>"
