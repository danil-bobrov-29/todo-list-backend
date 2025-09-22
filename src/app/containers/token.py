from dependency_injector import containers, providers

from src.app.core.db import AsyncTransaction
from src.app.domain.repositories.token import TokenRepository
from src.app.domain.services.token import TokenReader, TokenWrite
from src.app.security.token import TokenService


class TokenContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncTransaction)
    token_service = providers.Dependency(instance_of=TokenService)

    token_repository: TokenRepository = providers.Factory(
        TokenRepository,
        transaction=transaction,
    )

    token_reader = providers.Factory(
        TokenReader,
        token_repository=token_repository,
    )

    token_write: TokenWrite = providers.Factory(
        TokenWrite,
        token_repository=token_repository,
        token_service=token_service,
        token_reader=token_reader,
    )
