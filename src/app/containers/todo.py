from dependency_injector import containers, providers

from src.app.core.db import AsyncTransaction
from src.app.domain.repositories.todo import TodoRepository
from src.app.domain.services.todo import TodoCommand, TodoReader


class TodoContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncTransaction)

    todo_repository = providers.Factory(
        TodoRepository,
        transaction=transaction,
    )

    todo_reader = providers.Factory(
        TodoReader,
        todo_repository=todo_repository,
    )

    todo_command = providers.Factory(
        TodoCommand,
        todo_repository=todo_repository,
    )
