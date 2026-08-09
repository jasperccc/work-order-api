import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import EmailAlreadyRegisteredError
from app.repositories.user import UserRepository
from app.security import verify_password
from app.services.user import UserService


@pytest.mark.asyncio
async def test_register_creates_user_with_hashed_password(
    db_session: AsyncSession,
) -> None:
    repository = UserRepository(db_session)
    service = UserService(repository)

    user = await service.register(
        email="new@example.com",
        password="secure-password",
    )

    assert user.id is not None
    assert user.email == "new@example.com"
    assert user.password_hash != "secure-password"
    assert verify_password("secure-password", user.password_hash)

    persisted_user = await repository.get_by_email("new@example.com")

    assert persisted_user is not None
    assert persisted_user.id == user.id


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(
    db_session: AsyncSession,
) -> None:
    repository = UserRepository(db_session)
    service = UserService(repository)

    await service.register(
        email="duplicate@example.com",
        password="first-password",
    )

    with pytest.raises(EmailAlreadyRegisteredError) as exception_info:
        await service.register(
            email="duplicate@example.com",
            password="second-password",
        )
    assert str(exception_info.value) == "邮箱已注册"

    persisted_user = await repository.get_by_email("duplicate@example.com")

    assert persisted_user is not None
    assert verify_password("first-password", persisted_user.password_hash)
