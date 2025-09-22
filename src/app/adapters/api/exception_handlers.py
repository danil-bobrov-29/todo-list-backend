import functools

from fastapi import Request
from starlette.responses import JSONResponse

from src.app.adapters.api.schemas import SimpleApiError
from src.app.core.excetions import enums, errors


async def universal_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    response_content = SimpleApiError(
        success=False,
        code=enums.ErrorCodes.API_ERROR,
        message="Unknown error",
    ).model_dump()
    return JSONResponse(
        status_code=500,
        content=response_content,
    )


async def generic_exception_handler(request: Request, exc: errors.AppError) -> JSONResponse:
    response_content = exc.to_payload()
    partial_resp = functools.partial(JSONResponse, status_code=exc.status_code, content=response_content)
    if exc.headers:
        return partial_resp(exc.headers)  # type: ignore[misc]
    return partial_resp()


registry = [
    (errors.AppError, generic_exception_handler),
    (Exception, universal_exception_handler),
]
