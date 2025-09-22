from typing import Annotated, Literal
import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Query
from fastapi.params import Depends

from src.app.adapters.api.deps import current_user
from src.app.containers.container import Container
from src.app.domain.schemas.todo import (
    TodoBase,
    TodoCreate,
    TodoDetails,
    TodoQuery,
    TodosResponse,
    TodoUpdate,
    TodoWhereSchema,
)
from src.app.domain.services.todo import TodoCommand, TodoReader

router = APIRouter(prefix="/todo", tags=["Todos"])


@router.post(
    "",
    status_code=201,
    response_model=TodoDetails,
    summary="Создание новой задачи",
)
@inject
async def create_todo(
    todo: TodoBase,
    user_id: uuid.UUID = Depends(current_user),
    command: TodoCommand = Depends(Provide[Container.todo.todo_command]),  # type: ignore [attr-defined]
):
    return await command.create(
        TodoCreate.model_validate(
            {
                **todo.model_dump(),
                "user_id": user_id,
            }
        )
    )


@router.get(
    "/me",
    status_code=200,
    response_model=TodosResponse,
    summary="Получение всех задачей пользователя",
)
@inject
async def get_todos(
    user_id: uuid.UUID = Depends(current_user),
    query: TodoReader = Depends(Provide[Container.todo.todo_reader]),  # type: ignore [attr-defined]
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Сколько элементов на странице",
    ),
    sort_by: Annotated[
        Literal["created_at", "title"] | None,
        Query(
            description="Параметр для сортировки",
        ),
    ] = None,
    order_by: Annotated[
        Literal["desc", "asc"] | None,
        Query(
            description="Сортировка по убыванию/возрастанию",
        ),
    ] = None,
):
    return await query.get_todos_me(
        TodoQuery(
            page=page,
            limit=limit,
            order_by=order_by,
            sort_by=sort_by,
            filters=TodoWhereSchema(user_id=user_id),
        )
    )


@router.get(
    "/me/{todo_id}",
    status_code=200,
    response_model=TodoDetails,
    summary="Получение задачи пользователя по ID",
)
@inject
async def get_todo_by_id(
    todo_id: uuid.UUID,
    user_id: uuid.UUID = Depends(current_user),
    query: TodoReader = Depends(Provide[Container.todo.todo_reader]),  # type: ignore [attr-defined]
):
    return await query.get_todo_by_id_me(
        user_id=user_id,
        todo_id=todo_id,
    )


@router.patch(
    "/{todo_id}",
    status_code=204,
    summary="Изменение параметров задачи",
)
@inject
async def patch_todo(
    todo_id: uuid.UUID,
    payload: TodoUpdate,
    user_id: uuid.UUID = Depends(current_user),
    query: TodoReader = Depends(Provide[Container.todo.todo_reader]),  # type: ignore [attr-defined]
    command: TodoCommand = Depends(Provide[Container.todo.todo_command]),  # type: ignore [attr-defined]
):
    todo: TodoDetails = await query.get_todo_by_id_me(
        user_id=user_id,
        todo_id=todo_id,
    )
    await command.update(todo_id=todo.id, payload=payload)


@router.delete("/{todo_id}", status_code=204, summary="Удаление задачи")
@inject
async def delete_todo(
    todo_id: uuid.UUID,
    user_id: uuid.UUID = Depends(current_user),
    query: TodoReader = Depends(Provide[Container.todo.todo_reader]),  # type: ignore [attr-defined]
    command: TodoCommand = Depends(Provide[Container.todo.todo_command]),  # type: ignore [attr-defined]
):
    todo: TodoDetails = await query.get_todo_by_id_me(
        user_id=user_id,
        todo_id=todo_id,
    )

    await command.delete(todo_id=todo.id)


# Todo реализовать изменение
