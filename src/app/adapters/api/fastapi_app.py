from collections.abc import AsyncIterator
import contextlib
from typing import cast

from fastapi import FastAPI

from src.app.adapters.api import exception_handlers
from src.app.adapters.api.v1 import endpoints
from src.app.containers.container import Container
from src.app.core.config import Settings


@contextlib.asynccontextmanager
async def _lifespan(application: FastAPI) -> AsyncIterator[None]:
    container = cast(Container, application.extra["container"])
    if coro := container.init_resources():
        await coro
    yield
    if coro := container.shutdown_resources():
        await coro


def create_app():
    container = Container()
    config: Settings = Settings(**container.config())

    fastapi_application = FastAPI(
        title=config.app.name,
        version=config.app.version,
        container=container,
        lifespan=_lifespan,
    )

    fastapi_application.include_router(endpoints.router)

    for exc, handler in exception_handlers.registry:
        fastapi_application.add_exception_handler(exc, handler)

    return fastapi_application
