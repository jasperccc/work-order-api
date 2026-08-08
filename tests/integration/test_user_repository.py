import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_get_by_email_returns_existing_user(
    db_session: AsyncSession,
) -> None:
    existing_user = User(
        email="jasper@example.com",
        password_hash="hashed-password",
    )
    db_session.add(existing_user)
    await db_session.commit()

    repository = UserRepository(db_session)

    user = await repository.get_by_email("jasper@example.com")

    assert user is not None
    assert user.id == existing_user.id
    assert user.email == "jasper@example.com"


@pytest.mark.asyncio
async def test_get_by_email_returns_none_when_user_does_not_exist(
    db_session: AsyncSession,
) -> None:
    repository = UserRepository(db_session)
    user = await repository.get_by_email("missing@example.com")

    assert user is None


@pytest.mark.asyncio
async def test_add_makes_user_queryable(
    db_session: AsyncSession,
) -> None:
    repository = UserRepository(db_session)
    new_user = User(
        email="new@example.com",
        password_hash="hashed-password",
    )

    created_user = await repository.add(new_user)
    found_user = await repository.get_by_email("new@example.com")

    assert created_user.id is not None
    assert found_user is not None
    assert found_user.id == created_user.id
