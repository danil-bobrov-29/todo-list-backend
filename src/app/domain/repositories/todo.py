from src.app.domain.models import Todo
from src.app.domain.repositories.base import BaseRepository
from src.app.domain.schemas.todo import TodoWhereSchema


class TodoRepository(BaseRepository[Todo, TodoWhereSchema]):
    model = Todo
