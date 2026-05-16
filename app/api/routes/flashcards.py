from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.models.study_document import (
    StudyDocument
)

from app.models.flashcard import Flashcard

from app.core.dependencies import (
    get_current_user
)

from app.services.ai_service import (
    generate_flashcards
)

router = APIRouter()


@router.post("/generate/{document_id}")
def generate_document_flashcards(
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

    generated_flashcards = (
        generate_flashcards(
            document.content
        )
    )

    saved_flashcards = []

    for card in generated_flashcards:
        flashcard = Flashcard(
            question=card["question"],
            answer=card["answer"],
            document_id=document.id,
            owner_id=current_user.id
        )

        db.add(flashcard)

        saved_flashcards.append(
            flashcard
        )

    db.commit()

    return {
        "message": "Flashcards generated",
        "count": len(saved_flashcards)
    }


@router.get("/")
def get_flashcards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    flashcards = (
        db.query(Flashcard)
        .filter(
            Flashcard.owner_id == current_user.id
        )
        .all()
    )

    return flashcards