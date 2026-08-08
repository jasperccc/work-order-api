from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

# 管理连接池，确定连接的是哪一个数据库
engine = create_async_engine(
    settings.database_url,
    # 从连接池取出后先检查是否有效
    pool_pre_ping=True,
)

# 用于创建AsyncSession的工厂
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# 每次请求创建一个session，请求结束自动关闭
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session
