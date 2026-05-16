from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.websocket.manager import (
    manager
)

router = APIRouter()


@router.websocket("/chat")
async def websocket_chat(
    websocket: WebSocket
):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            await manager.send_message(
                f"AI: {data}",
                websocket
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)