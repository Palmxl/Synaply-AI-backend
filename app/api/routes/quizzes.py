from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.models.study_document import (
    StudyDocument
)

from app.models.quiz import Quiz

from app.models.quiz_question import (
    QuizQuestion
)

from app.core.dependencies import (
    get_current_user
)

from app.services.activity_service import log_activity
from app.services.ai_service import (
    generate_quiz
)

router = APIRouter()


@router.post("/generate/{document_id}")
def generate_document_quiz(
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

    generated_questions = (
        generate_quiz(
            document.content
        )
    )

    quiz = Quiz(
        title=f"{document.title} Quiz",
        owner_id=current_user.id,
        document_id=document.id
    )

    db.add(quiz)

    db.commit()

    db.refresh(quiz)

    for question in generated_questions:
        quiz_question = QuizQuestion(
            question=question["question"],
            option_a=question["option_a"],
            option_b=question["option_b"],
            option_c=question["option_c"],
            option_d=question["option_d"],
            correct_answer=question["correct_answer"],
            quiz_id=quiz.id
        )

        db.add(quiz_question)

    db.commit()

    log_activity(
        db=db,
        owner_id=current_user.id,
        action="generate_quiz",
        description=f"Generated quiz for {document.title}"
    )

    return {
        "message": "Quiz generated",
        "quiz_id": quiz.id,
    }

@router.get("/")
def get_user_quizzes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quizzes = (
        db.query(Quiz)
        .filter(
            Quiz.owner_id == current_user.id
        )
        .all()
    )

    return quizzes

@router.get("/{quiz_id}")
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.id == quiz_id,
            Quiz.owner_id == current_user.id
        )
        .first()
    )

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    questions = (
        db.query(QuizQuestion)
        .filter(
            QuizQuestion.quiz_id == quiz.id
        )
        .all()
    )

    return questions