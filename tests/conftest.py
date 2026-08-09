import os
from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

os.environ["WORK_ORDER_JWT_SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["WORK_ORDER_ENVIRONMENT"] = "test"
os.environ["WORK_ORDER_DATABASE_URL"] = (
    "postgresql+asyncpg://work_order_test:"
    "work_order_test_password@127.0.0.1:5435/work_order_test"
)

from app.config import settings
from app.database import get_session
from app.main import app
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


@pytest_asyncio.fixture
async def api_client(
    db_session: AsyncSession,
) -> AsyncIterator[AsyncClient]:
    async def override_get_session() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_session, None)
