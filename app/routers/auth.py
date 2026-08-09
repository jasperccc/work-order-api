from fastapi import APIRouter, status

from app.dependencies import UserServiceDependency
from app.schemas.user import TokenResponse, UserLogin, UserRegister, UserResponse
from app.security import create_access_token

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: UserRegister,
    service: UserServiceDependency,
) -> UserResponse:
    user = await service.register(
        email=data.email,
        password=data.password,
    )

    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    data: UserLogin,
    service: UserServiceDependency,
) -> TokenResponse:
    user = await service.authenticate(
        email=data.email,
        password=data.password,
    )
    access_token = create_access_token(str(user.id))

    return TokenResponse(access_token=access_token)
