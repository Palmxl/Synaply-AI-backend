from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.study_document import (
    StudyDocument
)

from app.models.user import User

from app.core.dependencies import (
    get_current_user
)

from app.services.activity_service import log_activity
from app.services.ai_service import (
    generate_summary
)

router = APIRouter()


@router.post("/summary/{document_id}")
def summarize_document(
    document_id: int,
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

    summary = generate_summary(
        document.content
    )

    log_activity(
        db=db,
        owner_id=current_user.id,
        action="generate_summary",
        description=f"Generated summary for {document.title}"
    )
    
    return {
        "summary": summary
    }