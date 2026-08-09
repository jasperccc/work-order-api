from sqlalchemy.exc import IntegrityError

from app.exceptions import EmailAlreadyRegisteredError
from app.models import User
from app.repositories.user import UserRepository
from app.security import hash_password


class UserService:
    """负责用户业务逻辑。"""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, email: str, password: str) -> User:
        """注册并保存用户。"""
        user = User(
            email=email,
            password_hash=hash_password(password),
        )
        try:
            created_user = await self.repository.add(user)
            await self.repository.commit()
        except IntegrityError as error:
            await self.repository.rollback()
            raise EmailAlreadyRegisteredError("邮箱已注册") from error
        except Exception:
            await self.repository.rollback()
            raise
        return created_user
