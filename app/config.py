import os
from dotenv import load_dotenv

# 1. Load the local .env file only if we aren't in production
load_dotenv()

# 2. Safely capture the runtime environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# 3. If Railway injected a production string, ensure it has the async driver prefix
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+asyncpg://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    # 4. Fallback exclusively for local offline development
    DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/chat_db"

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_default_key_for_local_dev")