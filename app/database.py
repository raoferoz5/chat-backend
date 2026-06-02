import os  # Ensure os is imported
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# 🚀 FIX: Force Railway's raw postgres URL to use the asyncpg driver prefix
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+asyncpg://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    # Local development fallback
    DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatapp"

# 1. Use create_async_engine with the sanitized async string
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  
    pool_pre_ping=True  
)

# 2. Configure the factory to build AsyncSessions instead of standard sessions
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()

# 3. Use an async generator to yield your database sessions cleanly
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()