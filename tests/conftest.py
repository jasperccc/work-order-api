import os
from collections.abc import AsyncIterator

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

os.environ["WORK_ORDER_ENVIRONMENT"] = "test"
os.environ["WORK_ORDER_DATABASE_URL"] = (
    "postgresql+asyncpg://work_order_test:"
    "work_order_test_password@127.0.0.1:5435/work_order_test"
)

from app.config import settings
from app.models import Base


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    test_engine = create_async_engine(settings.database_url)

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )

    try:
        async with session_factory() as session:
            yield session
    finally:
        async with test_engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

        await test_engine.dispose()
