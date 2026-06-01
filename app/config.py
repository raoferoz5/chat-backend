from dotenv import load_dotenv
import os

load_dotenv()

# Make sure the fallback looks like a real URL structure so SQLAlchemy won't crash on parsing
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:postgres@localhost:5432/chat_db"
)
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_default_key_for_local_dev")