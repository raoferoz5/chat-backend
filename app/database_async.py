# File path: app/database_async.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# NOTE: We use postgresql+asyncpg:// instead of postgresql:// for async support
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatapp"

# Create the asynchronous engine
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

# Set up the session factory used by our WebSocket loop
async_session_local = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_async_db():
    """Async database dependency generator"""
    async with async_session_local() as session:
        yield session