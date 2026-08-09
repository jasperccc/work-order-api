from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func, true
from sqlalchemy.orm import Mapped, mapped_column

from app.enums import UserRole
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            values_callable=lambda roles: [role.value for role in roles],
            native_enum=False,
            validate_strings=True,
            length=20,
        ),
        default=UserRole.USER,
        server_default=UserRole.USER.value,
    )
