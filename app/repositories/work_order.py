from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import WorkOrder


class WorkOrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, work_order: WorkOrder) -> WorkOrder:
        """将工单加入当前事务并执行INSERT。"""
        self.session.add(work_order)
        await self.session.flush()
        return work_order

    async def commit(self) -> None:
        """提交当前事务。"""
        await self.session.commit()

    async def rollback(self) -> None:
        """回滚当前事务。"""
        await self.session.rollback()

    async def list_by_owner_id(
        self,
        owner_id: int,
        limit: int,
        offset: int,
    ) -> list[WorkOrder]:
        statement = (
            select(WorkOrder)
            .where(WorkOrder.owner_id == owner_id)
            .order_by(WorkOrder.id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(statement)
        return list(result.all())

    async def get_by_id(self, work_order_id: int) -> WorkOrder | None:
        statement = select(WorkOrder).where(WorkOrder.id == work_order_id)
        result = await self.session.scalars(statement)
        return result.one_or_none()

    async def delete(self, work_order: WorkOrder) -> None:
        await self.session.delete(work_order)

    async def list_all(self) -> list[WorkOrder]:
        statement = select(WorkOrder).order_by(WorkOrder.id)
        result = await self.session.scalars(statement)
        return list(result.all())
