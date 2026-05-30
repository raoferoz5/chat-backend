import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy import select, desc, delete, update 
from sqlalchemy.orm import Session
from app.database import get_db
from app.database_async import async_session_local  # Imported for async websocket transactions
from app.models.chat_room import ChatRoom
from app.models.user import User      
from app.models.message import Message
from app.schemas.chat_room import RoomCreate
from app.schemas.message import MessageCreate
from app.services.dependencies import get_current_user
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from app.services.connection_manager import manager

router = APIRouter(
    prefix="/chat",
    tags=["Chat"], 
    responses={404: {"description": "Not found"}}
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


# STEP 6 UPGRADE: Returning clean sender usernames using relationships
@router.get("/messages/{room_id}")
async def get_messages(
    room_id: int,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    skip = (page - 1) * limit
    
    messages = (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .order_by(desc(Message.id))
        .offset(skip)
        .limit(limit)
        .all()
    )

    response = []
    for message in messages:
        response.append(
            {
                "id": message.id,
                "content": message.content,
                "sender_username": message.sender.username,  # Implicit ORM join
                "room_name": message.room.room_name,          # Implicit ORM join
                "is_read": message.is_read,
                "created_at": message.created_at.isoformat() if message.created_at else None
            }
        )

    return response


# ADVANCED UPGRADE: Async JSON Event Dispatcher Loop
@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await manager.connect(room_id, websocket)
    
    # Open an async context manager session to interact with Postgres without blocking
    async with async_session_local() as db:
        try:
            while True:
                raw_data = await websocket.receive_text()
                
                # FIXED: Wrapped all JSON parsing inside a single try/except block to protect against loop crashes
                try:
                    event = json.loads(raw_data)
                    event_type = event.get("type")
                    sender_id = event.get("sender_id")
                except json.JSONDecodeError:
                    continue  # Drop malformed string input safely

                # --- 1. NEW CHAT MESSAGE (Automated Storage) ---
                if event_type == "new_message":
                    content = event.get("content")
                    
                    # Store to Postgres automatically
                    new_msg = Message(content=content, sender_id=sender_id, room_id=room_id)
                    db.add(new_msg)
                    await db.commit()
                    await db.refresh(new_msg)

                    # Fetch sender username instantly using modern async statement execution
                    user_stmt = select(User.username).where(User.id == sender_id)
                    user_result = await db.execute(user_stmt)
                    username = user_result.scalar()

                    # Unified dictionary broadcast style across your connections manager
                    await manager.broadcast(room_id, {
                        "type": "new_message",
                        "message_id": new_msg.id,
                        "content": content,
                        "sender_id": sender_id,
                        "sender_username": username,
                        "created_at": str(new_msg.created_at)
                    })

                # --- 2. TYPING INDICATORS ---
                elif event_type == "typing":
                    is_typing = event.get("is_typing", False)
                    await manager.broadcast(room_id, {
                        "type": "typing",
                        "sender_id": sender_id,
                        "username": event.get("username", "Someone"),
                        "is_typing": is_typing
                    })

                # --- 3. READ RECEIPTS ---
                elif event_type == "read_receipt":
                    message_id = event.get("message_id")
                    
                    # Async update message record status
                    stmt = update(Message).where(Message.id == message_id).values(is_read=True)
                    await db.execute(stmt)
                    await db.commit()
                    
                    await manager.broadcast(room_id, {
                        "type": "read_receipt",
                        "message_id": message_id,
                        "is_read": True
                    })

                # --- 4. LIVE MESSAGE DELETION ---
                elif event_type == "delete_message":
                    message_id = event.get("message_id")
                    
                    # Delete statement with a safety constraint ensuring only the author can wipe it
                    del_stmt = delete(Message).where(Message.id == message_id, Message.sender_id == sender_id)
                    await db.execute(del_stmt)
                    await db.commit()

                    await manager.broadcast(room_id, {
                        "type": "delete_message",
                        "message_id": message_id
                    })

        except WebSocketDisconnect:
            manager.disconnect(room_id, websocket)


# STEP 10: Online User Counter Endpoint
@router.get("/rooms/{room_id}/online")
async def online_users(room_id: int):
    """
    Fetch the live count of currently connected users in a specific chat room.
    """
    return {
        "online_users": manager.room_users_count(room_id)
    }