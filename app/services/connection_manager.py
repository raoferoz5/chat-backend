from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.active_rooms = {}

    async def connect(
        self,
        room_id: int,
        websocket: WebSocket
    ):

        await websocket.accept()

        if room_id not in self.active_rooms:

            self.active_rooms[room_id] = []

        self.active_rooms[room_id].append(
            websocket
        )
    def room_users_count( self, room_id: int):
        return len(self.active_rooms.get(room_id, []))

    def disconnect(
        self,
        room_id: int,
        websocket: WebSocket
    ):

        self.active_rooms[room_id].remove(
            websocket
        )

    async def broadcast(
        self,
        room_id: int,
        message: str
    ):

        for connection in self.active_rooms.get(
            room_id,
            []
        ):

            await connection.send_text(
                message
            )


manager = ConnectionManager()