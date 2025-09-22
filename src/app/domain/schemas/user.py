from pydantic import Field

from src.app.domain.schemas.base import BaseModelSchema, BaseSchema


class UserWhereSchema(BaseSchema):
    email: str | None = None
    full_name: str | None = None


class UserBase(BaseSchema):
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserCreateModel(UserBase):
    hashed_password: str = Field(min_length=8)


class UserUpdate(BaseSchema):
    full_name: str | None = None


class UserDetail(BaseModelSchema, UserBase):
    hashed_password: str


class UserResponse(BaseModelSchema, UserBase): ...
