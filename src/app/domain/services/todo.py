import uuid

from pydantic import TypeAdapter

from src.app.core.excetions.errors import NotFoundAppError
from src.app.domain.models import Todo
from src.app.domain.repositories.todo import TodoRepository
from src.app.domain.schemas.todo import TodoCreate, TodoDetails, TodoQuery, TodosResponse, TodoUpdate, TodoWhereSchema


class TodoReader:
    def __init__(self, todo_repository: TodoRepository):
        self._todo_repository = todo_repository

    async def get_todos_me(
        self,
        payload: TodoQuery,
    ) -> TodosResponse:
        total, todos = await self._todo_repository.list(
            filters=payload.filters,
            **payload.model_dump(exclude={"filters"}),
        )

        todos_pd = TypeAdapter(list[TodoDetails]).validate_python(list(todos))

        return TodosResponse(
            page=payload.page,
            limit=payload.limit,
            total=total,
            todos=todos_pd,
        )

    async def get_todo_by_id_me(
        self,
        user_id: uuid.UUID,
        todo_id: uuid.UUID,
    ) -> TodoDetails:
        result: Todo | None = await self._todo_repository.get_by_id(
            id_=todo_id,
            filters=TodoWhereSchema(user_id=user_id),
        )

        if result is None:
            raise NotFoundAppError(
                details=f"Todo with this id {todo_id} does not exist",
            )

        return TodoDetails.model_validate(result)


class TodoCommand:
    def __init__(self, todo_repository: TodoRepository):
        self._todo_repository = todo_repository

    async def create(self, payload: TodoCreate) -> TodoDetails:
        new_todo = await self._todo_repository.create(
            obj_in=Todo(
                **payload.model_dump(),
            )
        )

        return TodoDetails.model_validate(new_todo)

    async def update(
        self,
        todo_id: uuid.UUID,
        payload: TodoUpdate,
    ) -> None:
        await self._todo_repository.update(id_=todo_id, payload=payload.model_dump(exclude_unset=True))

    async def delete(self, todo_id):
        await self._todo_repository.delete(id_=todo_id)
