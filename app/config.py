import os

# 1. Grab the raw environment string
RAW_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Sanitize it immediately at the source
if RAW_DATABASE_URL:
    if RAW_DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = RAW_DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif RAW_DATABASE_URL.startswith("postgresql://") and not RAW_DATABASE_URL.startswith("postgresql+asyncpg://"):
        DATABASE_URL = RAW_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatapp"