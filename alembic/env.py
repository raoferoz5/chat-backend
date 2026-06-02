import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

# Import app Base and Models for autogenerate detection
from app.database import Base  
from app.models import user, chat_room, message

# Alembic Config Object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Provide target metadata for autogenerate support
target_metadata = Base.metadata

# --- DYNAMIC DATABASE URL RESOLUTION ---
# 1. Look for Railway's injected environment variable first
db_url = os.getenv("DATABASE_URL")

if db_url:
    # Convert standard postgres handles to asyncpg-compatible drivers
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+asyncpg://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    # 2. Local fallback if no environment variable is present
    db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatapp"

# Inject the resolved clean URL back into the Alembic config state
config.set_main_option("sqlalchemy.url", db_url)
# ----------------------------------------


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
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
    url = config.get_main_option("sqlalchemy.url")
        
    print("Connecting to target database service engine context...")

    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())