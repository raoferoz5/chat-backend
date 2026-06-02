import os
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware  # 🚀 CRITICAL FOR RATE LIMITING

from app.database import engine, Base
from app.limiter import limiter  # Import your configured limiter
from app.models.chat_room import ChatRoom
from app.models.message import Message
from app.models.user import User
from app.routers.user import router as user_router
from app.routers.chat import router as chat_router

app = FastAPI(title="Chat Backend")

# 🚀 CRITICAL: Register SlowAPI configuration and middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include your routes
app.include_router(user_router)
app.include_router(chat_router)


@app.get("/")
async def home():
    return {"message": "Chat Backend Running"}


if __name__ == "__main__":
    import uvicorn
    # Read the dynamic port assigned by Railway, default to 8000 for local dev
    port = int(os.getenv("PORT", 8000))
    # Bind to 0.0.0.0 so the proxy can forward traffic outside the container
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)