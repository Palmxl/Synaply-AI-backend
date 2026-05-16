from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.dependencies import (
    get_current_user
)

from app.models.user import User

from app.models.study_document import (
    StudyDocument
)

from app.models.flashcard import Flashcard

from app.models.quiz import Quiz

from app.models.chat_message import (
    ChatMessage
)

from app.models.activity_log import (
    ActivityLog
)

router = APIRouter()


@router.get("/analytics")
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    total_documents = (
        db.query(StudyDocument)
        .filter(
            StudyDocument.owner_id
            == current_user.id
        )
        .count()
    )

    total_flashcards = (
        db.query(Flashcard)
        .filter(
            Flashcard.owner_id
            == current_user.id
        )
        .count()
    )

    total_quizzes = (
        db.query(Quiz)
        .filter(
            Quiz.owner_id
            == current_user.id
        )
        .count()
    )

    total_chat_messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.owner_id
            == current_user.id
        )
        .count()
    )

    activities = (
        db.query(ActivityLog)
        .filter(
            ActivityLog.owner_id
            == current_user.id
        )
        .order_by(
            ActivityLog.created_at.desc()
        )
        .limit(8)
        .all()
    )

    recent_activity = [
        {
            "action": activity.action,
            "description": activity.description,
            "created_at": (
                activity.created_at.isoformat()
            )
        }
        for activity in activities
    ]

    return {
        "total_documents":
            total_documents,

        "total_flashcards":
            total_flashcards,

        "total_quizzes":
            total_quizzes,

        "total_chat_messages":
            total_chat_messages,

        "recent_activity":
            recent_activity
    }