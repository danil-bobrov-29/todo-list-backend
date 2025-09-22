from dependency_injector.wiring import Provide, inject
from fastapi import Request
from fastapi.params import Depends

from src.app.containers.container import Container
from src.app.core.excetions.errors import UnauthorizedAppError
from src.app.domain.schemas.token import TokenPayload
from src.app.security.token import TokenService


@inject
def current_user(
    request: Request,
    token_service: TokenService = Depends(Provide[Container.token_service]),
):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise UnauthorizedAppError(details="Token is missing")

    payload: TokenPayload = token_service.decode_token(access_token)

    if not token_service.is_token_valid(payload.exp):
        raise UnauthorizedAppError(details="Token has expired")

    return payload.sub
