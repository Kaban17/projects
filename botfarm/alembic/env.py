import sys
from logging.config import fileConfig
from pathlib import Path
from typing import Any

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncConnection, AsyncEngine

from alembic import context

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# this is the Alembic Config object, which provides
# access to the values within the .ini file, as well as additional values
# from the command line.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import models
from app.models.user import Base  # noqa

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired as easy as: my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    import os

    url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations_online() -> None:
    """Run migrations in 'online' mode using async engine.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    import os

    configuration = config.get_section(config.config_ini_section)
    database_url = os.getenv("DATABASE_URL", configuration["sqlalchemy.url"])
    connectable: AsyncEngine = create_async_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: AsyncConnection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_async_migrations_online())
