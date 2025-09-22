from src.app.domain.models import User
from src.app.domain.repositories.base import BaseRepository
from src.app.domain.schemas.user import UserWhereSchema


class UserRepository(BaseRepository[User, UserWhereSchema]):
    model = User
