import asyncio
from logging.config import fileConfig
import os
import sys

from sqlalchemy import Connection, engine_from_config, pool
from sqlalchemy.engine import Connectable
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.app.core.config import settings
from src.app.domain import models

config = context.config
fileConfig(config.config_file_name)

target_metadata = models.Base.metadata  # type: ignore

if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", settings.db.database_url)


def do_run_migrations(connection: Connection) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def do_run_migrations_async(connectable: Connectable) -> None:
    async with connectable.connect() as conn:
        await conn.run_sync(do_run_migrations)


def run_migrations() -> None:
    connectable = context.config.attributes.get("connection")
    if not connectable:
        connectable = AsyncEngine(
            engine_from_config(
                config.get_section(config.config_ini_section),
                poolclass=pool.NullPool,
                future=True,
            ),
        )
    if isinstance(connectable, AsyncEngine):
        asyncio.run(do_run_migrations_async(connectable))
    else:
        do_run_migrations(connectable)


run_migrations()
