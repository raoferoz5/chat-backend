from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base # <-- Add declarative_base

import os

ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:eagl3786@localhost:5432/chatapp"

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

async_session_local = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# <-- Define your Base here so models can import it
Base = declarative_base() 

async def get_async_db():
    async with async_session_local() as session:
        yield session