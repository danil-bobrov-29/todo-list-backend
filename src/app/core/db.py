from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio.engine import (
    create_async_engine,
)


class AsyncTransaction:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)
        self.async_engine = create_async_engine(db_url)
        self.session_factory = async_sessionmaker(
            self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def use(
        self,
    ) -> AsyncGenerator[AsyncSession | Any, Any]:
        session = self.session_factory()
        try:
            async with session.begin():
                yield session
        finally:
            await session.close()
