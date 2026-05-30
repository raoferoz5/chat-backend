from pydantic import BaseModel


class ChatMessage(BaseModel):

    room_id: int

    message: str