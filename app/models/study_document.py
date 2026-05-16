from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from datetime import datetime

from app.db.database import Base


class StudyDocument(Base):
    __tablename__ = "study_documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    filename = Column(
        String,
        nullable=False
    )

    subject = Column(
        String,
        nullable=True
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    content = Column(
        Text,
        nullable=True
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )