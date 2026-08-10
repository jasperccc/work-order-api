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
