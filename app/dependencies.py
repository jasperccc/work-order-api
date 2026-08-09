from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.exceptions import InvalidTokenError
from app.models import User
from app.repositories.user import UserRepository
from app.security import decode_access_token
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

bearer_scheme = HTTPBearer()

BearerCredentialsDependency = Annotated[
    HTTPAuthorizationCredentials,
    Depends(bearer_scheme),
]


async def get_current_user(
    credentials: BearerCredentialsDependency,
    session: SessionDependency,
) -> User:
    token = credentials.credentials
    subject = decode_access_token(token)
    try:
        user_id = int(subject)
    except ValueError as error:
        raise InvalidTokenError("认证凭证无效") from error

    repository = UserRepository(session)
    user = await repository.get_by_id(user_id)

    if user is None or not user.is_active:
        raise InvalidTokenError("认证凭证无效")
    return user


CurrentUserDependency = Annotated[
    User,
    Depends(get_current_user),
]
