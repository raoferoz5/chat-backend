# app/redis_config.py
import redis.asyncio as aioredis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create an async redis client instance
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)