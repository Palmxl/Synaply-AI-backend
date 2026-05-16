from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user

from app.models.user import User

from app.db.database import get_db

from app.models.study_document import StudyDocument

from app.services.pdf_service import save_pdf

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filename = await save_pdf(file)

    document = StudyDocument(
        title=file.filename,
        filename=filename,
        subject="General",
        owner_id=current_user.id
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    return {
        "message": "Document uploaded successfully"
    }


@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = (
        db.query(StudyDocument)
        .filter(
            StudyDocument.owner_id == current_user.id
        )
        .all()
    )

    return documents