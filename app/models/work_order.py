from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.enums import WorkOrderStatus
from app.models.base import Base


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[WorkOrderStatus] = mapped_column(
        Enum(
            WorkOrderStatus,
            values_callable=lambda roles: [role.value for role in roles],
            native_enum=False,
            validate_strings=True,
            length=20,
        ),
        default=WorkOrderStatus.OPEN,
        server_default=WorkOrderStatus.OPEN.value,
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
