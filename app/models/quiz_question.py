from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.db.database import Base


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        String,
        nullable=False
    )

    option_a = Column(
        String,
        nullable=False
    )

    option_b = Column(
        String,
        nullable=False
    )

    option_c = Column(
        String,
        nullable=False
    )

    option_d = Column(
        String,
        nullable=False
    )

    correct_answer = Column(
        String,
        nullable=False
    )

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id")
    )