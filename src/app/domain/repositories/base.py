from collections.abc import Sequence
from typing import Any, Generic, Literal, TypeVar
import uuid

from pydantic import BaseModel
from sqlalchemy import delete as sa_delete
from sqlalchemy import func, select
from sqlalchemy import update as sa_update
from sqlalchemy.orm import InstrumentedAttribute

from src.app.core.db import AsyncTransaction

ModelT = TypeVar("ModelT")
FilterSchemaT = TypeVar("FilterSchemaT", bound=BaseModel)


class BaseRepository(Generic[ModelT, FilterSchemaT]):
    model: ModelT

    def __init__(self, transaction: AsyncTransaction):
        self._transaction = transaction

    def _col(self, name: str) -> InstrumentedAttribute:
        return getattr(self.model, name)

    def _apply_filters(self, stmt, filters: FilterSchemaT | None):
        if not filters:
            return stmt
        for key, value in filters.model_dump(exclude_unset=True).items():
            col = self._col(key)
            stmt = stmt.where(col.ilike(value)) if isinstance(value, str) and "%" in value else stmt.where(col == value)
        return stmt

    async def get_by_id(
        self,
        id_: uuid.UUID | None,
        filters: FilterSchemaT | None = None,
    ) -> ModelT | None:
        stmt = select(self.model)

        if filters:
            stmt = self._apply_filters(stmt, filters)

        async with self._transaction.use() as session:
            result = await session.execute(stmt.where(self._col("id") == id_))

        return result.scalar_one_or_none()

    async def get_one_or_none(self, filters: FilterSchemaT) -> ModelT | None:
        stmt = select(self.model)
        stmt = self._apply_filters(stmt, filters)

        async with self._transaction.use() as session:
            result = await session.execute(stmt)

        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        page: int = 1,
        limit: int = 20,
        filters: FilterSchemaT | None = None,
        sort_by: str | None = None,
        order_by: Literal["desc", "asc"] | None = None,
    ) -> tuple[int, Sequence[ModelT]]:
        stmt = select(self.model)
        stmt = self._apply_filters(stmt, filters)

        async with self._transaction.use() as session:
            total = await session.execute(
                select(func.count()).select_from(stmt.subquery()),
            )
            if sort_by:
                col = self._col(sort_by)
                stmt = stmt.order_by(col.desc() if order_by == "desc" else col.asc())

            stmt = stmt.offset((page - 1) * limit).limit(limit)
            result = await session.execute(stmt)

        return total.scalar() or 0, result.scalars().all()

    async def create(self, obj_in: ModelT) -> ModelT:
        async with self._transaction.use() as session:
            session.add(obj_in)
            await session.flush()
            await session.refresh(obj_in)

        return obj_in

    async def update(
        self,
        id_: uuid.UUID,
        payload: dict[str, Any],
    ) -> None:
        stmt = sa_update(self.model)
        if id_ is not None:
            stmt = stmt.where(id_ == self.model.id)

        stmt = stmt.values(**payload)
        async with self._transaction.use() as session:
            await session.execute(stmt)


    async def delete(self, id_: Any) -> None:
        stmt = sa_delete(self.model).where(self._col("id") == id_)
        async with self._transaction.use() as session:
            await session.execute(stmt)

