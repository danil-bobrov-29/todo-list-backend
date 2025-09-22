from dependency_injector import containers, providers

from src.app.core.db import AsyncTransaction
from src.app.domain.repositories.user import UserRepository
from src.app.domain.services.token import TokenWrite
from src.app.domain.services.user import UserService
from src.app.security.password import PasswordService


class UserContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncTransaction)
    password_service = providers.Dependency(instance_of=PasswordService)
    token_write = providers.Dependency(instance_of=TokenWrite)

    user_repository = providers.Factory(UserRepository, transaction=transaction)

    user_service = providers.Factory(
        UserService, repository=user_repository, password_service=password_service, token_write=token_write
    )
