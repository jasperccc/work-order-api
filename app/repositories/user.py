from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserRepository:
    """负责访问用户数据。"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """根据邮箱查询用户。"""
        statement = select(User).where(User.email == email)
        result = await self.session.scalars(statement)
        return result.one_or_none()

    async def add(self, user: User) -> User:
        """将用户加入当前事务并执行INSERT。"""
        self.session.add(user)
        await self.session.flush()
        return user

    async def commit(self) -> None:
        """提交当前事务。"""
        await self.session.commit()

    async def rollback(self) -> None:
        """回滚当前事务。"""
        await self.session.rollback()

    async def get_by_id(self, user_id: int) -> User | None:
        """查询用户id"""
        statement = select(User).where(User.id == user_id)
        result = await self.session.scalars(statement)
        return result.one_or_none()
