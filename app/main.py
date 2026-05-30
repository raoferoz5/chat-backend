from fastapi import FastAPI
from app.models.chat_room import ChatRoom
from app.models.message import Message
from app.database import engine, Base
from app.models.user import User
from app.routers.user import router as user_router
from app.routers.chat import router as chat_router


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
app.include_router(chat_router)


@app.get("/")
async def home():
    return {"message": "Chat Backend Running"}