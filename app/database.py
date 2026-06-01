from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# 1. Use create_async_engine for non-blocking database queries
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True if you want to see raw SQL logs in Railway
    pool_pre_ping=True  # Automatically checks and revives dead connections
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