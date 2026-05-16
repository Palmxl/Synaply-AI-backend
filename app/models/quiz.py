from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.db.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    document_id = Column(
        Integer,
        ForeignKey("study_documents.id")
    )