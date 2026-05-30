from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "fallback_default_url_for_local_dev")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_default_key_for_local_dev")