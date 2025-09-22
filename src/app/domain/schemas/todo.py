from typing import Literal
import uuid

from pydantic import ConfigDict, Field

from src.app.domain.schemas.base import BaseModelSchema, BaseSchema


class TodoWhereSchema(BaseSchema):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None
    user_id: uuid.UUID | None = None


class TodoBase(BaseSchema):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class TodoDetails(BaseModelSchema):
    title: str
    description: str | None = None
    is_done: bool
    user_id: uuid.UUID


class TodoCreate(TodoBase):
    user_id: uuid.UUID


class TodoQuery(BaseSchema):
    page: int
    limit: int
    filters: TodoWhereSchema
    sort_by: str | None = None
    order_by: Literal["desc", "asc"] | None = None

class TodoUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None


class TodosResponse(BaseSchema):
    page: int
    limit: int
    total: int
    todos: list[TodoDetails]


class TodoOut(TodoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: uuid.UUID
