from fastapi import APIRouter, status

from app.dependencies import CurrentUserDependency, WorkOrderServiceDependency
from app.schemas.work_order import WorkOrderCreate, WorkOrderResponse

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
