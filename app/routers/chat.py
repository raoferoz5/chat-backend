from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy import select, desc  # FIXED: Added select and desc imports
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chat_room import ChatRoom
from app.models.user import User      # FIXED: Added User model import
from app.models.message import Message

from app.schemas.chat_room import RoomCreate
from app.schemas.message import MessageCreate
from app.services.dependencies import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/rooms")
async def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_room = db.query(ChatRoom).filter(
        ChatRoom.room_name == room.room_name
    ).first()

    if existing_room:
        raise HTTPException(
            status_code=400,
            detail="Room already exists"
        )

    new_room = ChatRoom(
        room_name=room.room_name
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return {
        "message": "Room created successfully",
        "room_id": new_room.id
    }


@router.get("/rooms")
async def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(ChatRoom).all()
    return rooms


@router.post("/messages")
async def send_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    room = db.query(ChatRoom).filter(
        ChatRoom.id == message.room_id
    ).first()

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    # Defensive check depending on how current_user is passed (object vs dict)
    try:
        sender_id = current_user.id
    except AttributeError:
        sender_id = current_user["user_id"]

    new_message = Message(
        content=message.content,
        sender_id=sender_id,
        room_id=message.room_id
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return {
        "message": "Message sent successfully"
    }


@router.get("/messages/{room_id}")
async def get_messages(
    room_id: int,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    # Verify room existence first
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    skip = (page - 1) * limit
    
    # FIXED: Cleaned up duplicate lines, case typos, and built the statement correctly
    statement = (
        select(
            Message.id,
            Message.content,
            Message.room_id,
            Message.sender_id,
            User.username.label("sender_username"),   # Capital 'U'
            ChatRoom.room_name.label("room_name")
        )
        .join(User, Message.sender_id == User.id)
        .join(ChatRoom, Message.room_id == ChatRoom.id)
        .filter(Message.room_id == room_id)
        .order_by(desc(Message.id))
        .offset(skip)
        .limit(limit)
    )

    # FIXED: Exchanged legacy query for executing the modern joined query statement
    result = db.execute(statement)
    messages = result.mappings().all()

    return messages