import uuid

from src.app.core.excetions.errors import NotFoundAppError, UnauthorizedAppError
from src.app.domain.models import Token
from src.app.domain.repositories.token import TokenRepository
from src.app.domain.schemas.token import (
    TokenDetails,
    TokenPair,
    TokenPayload,
    TokenWhereSchema,
)
from src.app.domain.schemas.user import UserDetail
from src.app.security.token import TokenService


class TokenReader:
    def __init__(
        self,
        token_repository: TokenRepository,
    ):
        self._token_repository = token_repository

    async def get_token_by_user(self, user_id: uuid.UUID) -> TokenDetails:
        token = await self._token_repository.get_one_or_none(
            filters=TokenWhereSchema(user_id=user_id),
        )
        if not token:
            raise NotFoundAppError(details="This user does not have a token")

        return TokenDetails.model_validate(token)


class TokenWrite:
    def __init__(
        self,
        token_repository: TokenRepository,
        token_service: TokenService,
        token_reader: TokenReader,
    ):
        self._token_repository = token_repository
        self._token_service = token_service
        self._token_reader = token_reader

    async def create_token(self, user: UserDetail) -> TokenPair:
        try:
            token: TokenDetails = await self._token_reader.get_token_by_user(
                user.id,
            )
            params_token: TokenPayload = self._token_service.decode_token(
                token.refresh_token,
            )

            if not self._token_service.is_token_valid(params_token.exp):
                raise UnauthorizedAppError(details="Token has expired")
            refresh_token = token.refresh_token

        except (UnauthorizedAppError, NotFoundAppError):
            refresh_token: str = self._token_service.create_refresh_token(
                str(user.id),
            )
            await self._token_repository.create(
                Token(
                    user_id=user.id,
                    refresh_token=refresh_token,
                )
            )

        access_token = self._token_service.create_access_token(str(user.id))

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, token: str) -> TokenPair:
        data: TokenPayload = self._token_service.decode_token(token)

        if data.type == "refresh" and self._token_service.is_token_valid(exp_ts=data.exp):
            token: TokenDetails = await self._token_reader.get_token_by_user(data.sub)

        new_access_token = self._token_service.create_access_token(str(token.user_id))

        return TokenPair(
            access_token=new_access_token,
            refresh_token=token.refresh_token,
        )
