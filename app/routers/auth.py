from fastapi import APIRouter, status

from app.dependencies import UserServiceDependency
from app.schemas.user import UserRegister, UserResponse

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
