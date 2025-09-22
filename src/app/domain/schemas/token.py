import uuid

from src.app.domain.schemas.base import BaseModelSchema, BaseSchema


class TokenWhereSchema(BaseSchema):
    user_id: uuid.UUID | None = None
    refresh_token: str | None = None


class TokenDetails(BaseModelSchema):
    user_id: uuid.UUID
    refresh_token: str


class TokenUpdate(BaseSchema):
    access_token: str
    token_type: str
    expires_in: int


class TokenPair(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseSchema):
    sub: uuid.UUID
    type: str
    exp: int
