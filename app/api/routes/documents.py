from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user

from app.models.user import User

from app.db.database import get_db

from app.models.study_document import StudyDocument
from app.models.document_chunk import (
    DocumentChunk
)

from app.services.pdf_service import (
    save_pdf,
    extract_text_from_pdf
)

from app.services.chunk_service import (
    chunk_text
)

from app.services.vector_service import (
    add_document_chunk
)

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filename, file_path = await save_pdf(file)

    extracted_text = extract_text_from_pdf(
        file_path
    )

    chunks = chunk_text(extracted_text)

    document = StudyDocument(
        title=file.filename,
        filename=filename,
        subject="General",
        owner_id=current_user.id,
        content=extracted_text
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    for index, chunk in enumerate(chunks):
        document_chunk = DocumentChunk(
            content=chunk,
            chunk_index=index,
            document_id=document.id
        )

        db.add(document_chunk)

        add_document_chunk(
            chunk_id=f"{document.id}_{index}",
            content=chunk,
            document_id=document.id
        )

    db.commit()

    return {
        "message": "Document uploaded successfully",
        "characters": len(extracted_text),
        "chunks": len(chunks)
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