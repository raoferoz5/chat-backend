#!/bin/sh

# 1. Force alembic to clear any stuck states and upgrade the database
echo "Clearing old migration tracking stamps..."
alembic stamp head

echo "Applying latest database migrations..."
alembic upgrade head

# 2. Start the FastAPI application layer
echo "Starting FastAPI production web server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000