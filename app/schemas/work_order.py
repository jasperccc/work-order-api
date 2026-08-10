from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums import WorkOrderStatus


class WorkOrderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class WorkOrderResponse(BaseModel):
    id: int
    title: str
    status: WorkOrderStatus
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
