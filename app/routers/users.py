from fastapi import APIRouter

from app.dependencies import CurrentUserDependency
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
async def read_current_user(
    current_user: CurrentUserDependency,
) -> UserResponse:
    return UserResponse.model_validate(current_user)
