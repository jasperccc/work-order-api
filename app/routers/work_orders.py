from fastapi import APIRouter, status

from app.dependencies import CurrentUserDependency, WorkOrderServiceDependency
from app.schemas.work_order import (
    WorkOrderCreate,
    WorkOrderResponse,
    WorkOrderUpdate,
)

router = APIRouter(
    prefix="/api/work-orders",
    tags=["work-orders"],
)


@router.post(
    "",
    response_model=WorkOrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_work_order(
    data: WorkOrderCreate,
    current_user: CurrentUserDependency,
    service: WorkOrderServiceDependency,
) -> WorkOrderResponse:
    work_order = await service.create(
        title=data.title,
        owner_id=current_user.id,
    )
    return WorkOrderResponse.model_validate(work_order)


@router.get(
    "",
    response_model=list[WorkOrderResponse],
)
async def list_work_orders(
    current_user: CurrentUserDependency,
    service: WorkOrderServiceDependency,
) -> list[WorkOrderResponse]:
    work_orders = await service.list_for_user(current_user.id)

    return [WorkOrderResponse.model_validate(work_order) for work_order in work_orders]


@router.get(
    "/{work_order_id}",
    response_model=WorkOrderResponse,
)
async def get_work_order(
    work_order_id: int,
    current_user: CurrentUserDependency,
    service: WorkOrderServiceDependency,
) -> WorkOrderResponse:
    work_order = await service.get_for_user(work_order_id, current_user.id)
    return WorkOrderResponse.model_validate(work_order)


@router.patch(
    "/{work_order_id}",
    response_model=WorkOrderResponse,
)
async def update_work_order(
    work_order_id: int,
    data: WorkOrderUpdate,
    current_user: CurrentUserDependency,
    service: WorkOrderServiceDependency,
) -> WorkOrderResponse:
    work_order = await service.update_for_user(
        work_order_id=work_order_id,
        owner_id=current_user.id,
        title=data.title,
    )
    return WorkOrderResponse.model_validate(work_order)


@router.delete(
    "/{work_order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_work_order(
    work_order_id: int,
    current_user: CurrentUserDependency,
    service: WorkOrderServiceDependency,
) -> None:
    await service.delete_for_user(
        work_order_id=work_order_id,
        owner_id=current_user.id,
    )
