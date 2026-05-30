from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class ChatRoom(Base):

    __tablename__ = "chat_rooms"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    room_name = Column(
        String(100),
        unique=True,
        nullable=False
    )
    messages = relationship(
    "Message",
    back_populates="room"
)