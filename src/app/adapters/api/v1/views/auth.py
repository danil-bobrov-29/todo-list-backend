from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Cookie, Depends

from src.app.containers.container import Container
from src.app.core.excetions.errors import ConflictAppError, UnauthorizedAppError
from src.app.domain.schemas.auth import LoginIn
from src.app.domain.schemas.token import TokenPair
from src.app.domain.schemas.user import UserCreate, UserDetail, UserResponse
from src.app.domain.services.token import TokenWrite
from src.app.domain.services.user import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    status_code=201,
    response_model=UserResponse,
    summary="Регистрация",
)
@inject
async def register(
    payload: UserCreate,
    user_service: UserService = Depends(Provide[Container.user.user_service]),  # type: ignore [attr-defined]
):
    return await user_service.create_user(payload)


@router.post(
    "/login",
    status_code=200,
    response_model=TokenPair,
    summary="Авторизация",
)
@inject
async def login(
    payload: LoginIn,
    user_service: UserService = Depends(Provide[Container.user.user_service]),  # type: ignore [attr-defined]
):
    return await user_service.authenticate_user(**payload.model_dump())


@router.post(
    "/refresh",
    status_code=201,
    response_model=TokenPair,
    summary="Перезапись токена",
)
@inject
async def refresh(
    refresh_cookie: str | None = Cookie(default=None, alias="refresh_token"),
    token_writer: TokenWrite = Depends(Provide[Container.token.token_write]),  # type: ignore [attr-defined]
):
    if not refresh_cookie:
        raise UnauthorizedAppError(details="Missing refresh token cookie")

    return await token_writer.refresh(refresh_cookie)
