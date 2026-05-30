# File path: app/schemas/message.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    room_id: int
    content: str = Field(..., min_length=1, description="Message text cannot be empty")

    @field_validator('content')
    @classmethod
    def prevent_whitespace_only(cls, value: str) -> str:
        # Strip trailing/leading spaces and check if anything is left
        if not value.strip():
            raise ValueError("Message content cannot consist of empty spaces only.")
        return value

class MessageResponse(BaseModel):
    id: int
    content: str = Field(min_length=1, max_length=1000)
    sender_username: str  # FIXED: Changed from StopIteration to str, and matched Step 6's name
    room_name: str
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read from SQLAlchemy ORM models smoothly