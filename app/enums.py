from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class WorkOrderStatus(StrEnum):
    OPEN = "open"
