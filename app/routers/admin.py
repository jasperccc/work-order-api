from fastapi import APIRouter

from app.dependencies import AdminUserDependency, WorkOrderServiceDependency
from app.schemas.work_order import WorkOrderResponse

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
)


@router.get(
    "/work-orders",
    response_model=list[WorkOrderResponse],
)
async def list_all_work_orders(
    _current_admin: AdminUserDependency,
    service: WorkOrderServiceDependency,
) -> list[WorkOrderResponse]:
    work_orders = await service.list_all()
    return [WorkOrderResponse.model_validate(work_order) for work_order in work_orders]
