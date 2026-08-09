from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.user import UserRepository
from app.services.user import UserService

SessionDependency = Annotated[
    AsyncSession,
    Depends(get_session),
]


async def get_user_service(
    session: SessionDependency,
) -> UserService:
    repository = UserRepository(session)
    return UserService(repository)


UserServiceDependency = Annotated[
    UserService,
    Depends(get_user_service),
]
