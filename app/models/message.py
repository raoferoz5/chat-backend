from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base
from sqlalchemy.orm import relationship

class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    content = Column(
        String,
        nullable=False
    )

    sender_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    room_id = Column(
        Integer,
        ForeignKey("chat_rooms.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    sender = relationship(
    "User",
    back_populates="messages"
    )

    room = relationship(
        "ChatRoom",
        back_populates="messages"
    )