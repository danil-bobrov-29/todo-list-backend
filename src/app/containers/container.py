from dependency_injector import containers, providers

from src.app.containers.todo import TodoContainer
from src.app.containers.token import TokenContainer
from src.app.containers.user import UserContainer
from src.app.core.config import Settings
from src.app.core.db import AsyncTransaction
from src.app.security.password import PasswordService
from src.app.security.token import TokenService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.app.adapters.api.v1.views.auth",
            "src.app.adapters.api.v1.views.todo",
        ]
    )

    config = providers.Configuration()
    config.from_dict(Settings().model_dump())

    transaction = providers.Singleton(
        AsyncTransaction,
        db_url=config.db.database_url,
    )

    password_service = providers.Factory(PasswordService)

    token_service = providers.Factory(
        TokenService,
        security_settings=config.security,
    )

    token = providers.Container(
        TokenContainer,
        transaction=transaction,
        token_service=token_service,
    )

    user = providers.Container(
        UserContainer,
        transaction=transaction,
        password_service=password_service,
        token_write=token.token_write,
    )

    todo = providers.Container(
        TodoContainer,
        transaction=transaction,
    )
