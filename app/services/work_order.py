from app.exceptions import WorkOrderNotFoundError
from app.models import WorkOrder
from app.repositories.work_order import WorkOrderRepository


class WorkOrderService:
    def __init__(self, repository: WorkOrderRepository):
        self.repository = repository

    async def create(self, title: str, owner_id: int) -> WorkOrder:
        work_order = WorkOrder(title=title, owner_id=owner_id)
        try:
            created_order = await self.repository.add(work_order)
            await self.repository.commit()
        except Exception:
            await self.repository.rollback()
            raise
        return created_order

    async def list_for_user(self, owner_id: int) -> list[WorkOrder]:
        return await self.repository.list_by_owner_id(owner_id)

    async def get_for_user(
        self,
        work_order_id: int,
        owner_id: int,
    ) -> WorkOrder:
        work_order = await self.repository.get_by_id(work_order_id)
        if work_order is None or work_order.owner_id != owner_id:
            raise WorkOrderNotFoundError("工单不存在")
        return work_order
