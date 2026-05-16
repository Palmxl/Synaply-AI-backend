import json

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.websocket.manager import (
    manager
)

from app.services.ai_service import (
    stream_chat_with_document
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

            payload = json.loads(data)

            document_id = payload[
                "document_id"
            ]

            question = payload[
                "question"
            ]

            stream = (
                stream_chat_with_document(
                    document_id=document_id,
                    question=question
                )
            )

            for chunk in stream:
                content = chunk["message"][
                    "content"
                ]

                if not content:
                    continue

                await manager.send_message(
                    content,
                    websocket
                )

            await manager.send_message(
                "[DONE]",
                websocket
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)