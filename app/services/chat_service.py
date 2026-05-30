from app.models.message import Message


def save_message(
    db,
    room_id,
    sender_id,
    content
):

    message = Message(
        room_id=room_id,
        sender_id=sender_id,
        content=content
    )

    db.add(message)

    db.commit()

    db.refresh(message)

    return message