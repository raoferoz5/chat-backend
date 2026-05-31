import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config, create_async_engine

# Import app Base and Models for autogenerate detection
from app.database import Base  
from app.models import user, chat_room, message

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Assign metadata so Alembic can automatically detect schema changes
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    
    # URL Driver Patch: Offline mode needs standard postgresql:// instead of asyncpg
    if url and url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql+asyncpg://", "postgresql://")
        
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Helper function to run the actual migrations inside the async context."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an AsyncEngine."""
    
    # Pull the Async URL from the environment, fallback to local dev string if missing
    # Change this line in alembic/env.py to match your local setup exactly:
    db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/chatapp")
    
    if db_url and db_url != "%(DATABASE_URL)s":
        connectable = create_async_engine(
            db_url,
            poolclass=pool.NullPool,
        )
    else:
        setting_dict = config.get_section(config.config_ini_section, {})
        connectable = async_engine_from_config(
            setting_dict,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())