from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.db.database import Base


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        String,
        nullable=False
    )

    answer = Column(
        String,
        nullable=False
    )

    document_id = Column(
        Integer,
        ForeignKey("study_documents.id")
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )