from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.chat_room import ChatRoom
from app.schemas.chat_room import RoomCreate
from app.services.dependencies import (
    get_current_user
)
from app.models.message import Message

from app.schemas.message import (
    MessageCreate
)

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

    new_message = Message(
        content=message.content,
        sender_id=current_user["user_id"],
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

    skip = (page - 1) * limit

    messages = db.query(Message).filter(
        Message.room_id == room_id
    ).offset(skip).limit(limit).all()

    return messages