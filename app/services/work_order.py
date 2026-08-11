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
