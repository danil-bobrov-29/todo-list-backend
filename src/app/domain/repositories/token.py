from src.app.domain.models import Token
from src.app.domain.repositories.base import BaseRepository
from src.app.domain.schemas.token import TokenWhereSchema


class TokenRepository(BaseRepository[Token, TokenWhereSchema]):
    model = Token
