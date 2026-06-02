import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config, create_async_engine

# Import app Base and Models for autogenerate detection
from app.database import Base  
from app.models import user, chat_room, message

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an AsyncEngine."""
    
    # 1. Pull the URL from the environment
    db_url = os.getenv("DATABASE_URL")
    
    # 2. If it exists, make sure it uses the asyncpg driver prefix
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+asyncpg://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        # 3. Fallback for your local development setup
        db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatapp"
        
    # Keep the rest of your original engine setup exactly the same:
    connectable = create_async_engine(
        db_url,
        poolclass=pool.NullPool,
    )