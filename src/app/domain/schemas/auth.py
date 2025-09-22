from pydantic import BaseModel, Field


class LoginIn(BaseModel):
    email: str
    password: str = Field(min_length=8)


class RegisterIn(LoginIn):
    full_name: str | None = None


class TokenDetail(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
