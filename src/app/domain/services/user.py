import uuid

from src.app.core.excetions.errors import UnauthorizedAppError, ConflictAppError
from src.app.domain.models import User
from src.app.domain.repositories.user import UserRepository
from src.app.domain.schemas.token import TokenPair
from src.app.domain.schemas.user import UserCreate, UserDetail, UserWhereSchema, UserResponse
from src.app.domain.services.token import TokenWrite
from src.app.security.password import PasswordService


class UserService:
    def __init__(
        self,
        repository: UserRepository,
        password_service: PasswordService,
        token_write: TokenWrite,
    ):
        self._repository = repository
        self._password_service = password_service
        self._token_write = token_write

    async def get_user(self, user_id: uuid.UUID) -> User:
        return await self._repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> UserDetail | None:
        existing_user: User | None = await self._repository.get_one_or_none(
            filters=UserWhereSchema(email=email),
        )

        return UserDetail.model_validate(existing_user) if existing_user else None

    async def create_user(self, user: UserCreate) -> UserResponse:
        existing_user: UserDetail | None = await self.get_user_by_email(
            user.email
        )

        if existing_user is not None:
            raise ConflictAppError(details="User already exists")

        hashed_password = self._password_service.hash_password(user.password)

        created_user: User = await self._repository.create(
            obj_in=User(
                hashed_password=hashed_password,
                **user.model_dump(exclude={"password"})
            )
        )

        return UserResponse.model_validate(created_user)

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> TokenPair:
        existing_users: UserDetail | None = await self.get_user_by_email(email)

        if existing_users and self._password_service.verify_password(
            password=password,
            hashed=existing_users.hashed_password,
        ):
            return await self._token_write.create_token(existing_users)

        raise UnauthorizedAppError(details="Invalid credentials")
