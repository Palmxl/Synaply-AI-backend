from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.models.study_document import (
    StudyDocument
)

from app.models.chat_message import (
    ChatMessage
)

from app.core.dependencies import (
    get_current_user
)

from app.schemas.chat import (
    ChatRequest
)

from app.services.activity_service import log_activity
from app.services.ai_service import (
    chat_with_document
)

router = APIRouter()


@router.post("/{document_id}")
def document_chat(
    document_id: int,
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = (
        db.query(StudyDocument)
        .filter(
            StudyDocument.id == document_id,
            StudyDocument.owner_id == current_user.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    answer = chat_with_document(
        document.id,
        payload.question
    )

    user_message = ChatMessage(
        role="user",
        content=payload.question,
        document_id=document.id,
        owner_id=current_user.id
    )

    assistant_message = ChatMessage(
        role="assistant",
        content=answer,
        document_id=document.id,
        owner_id=current_user.id
    )

    db.add(user_message)
    db.add(assistant_message)

    db.commit()

    log_activity(
        db=db,
        owner_id=current_user.id,
        action="chat_message",
        description=f"Asked AI about {document.title}"
    )
    
    return {
        "answer": answer
    }