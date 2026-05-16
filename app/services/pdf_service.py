import os

from fastapi import UploadFile

from pypdf import PdfReader

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_pdf(file: UploadFile):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        content = await file.read()

        buffer.write(content)

    return file.filename, file_path


def extract_text_from_pdf(
    file_path: str
):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text