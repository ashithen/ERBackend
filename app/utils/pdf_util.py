import tempfile

from PyPDF2 import PdfReader
from fastapi import UploadFile

from app.core.config import settings


# def extract_text_from_pdf(upload_file: UploadFile) -> str:
#     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#         temp_file.write(upload_file.file.read())
#         md_text = pymupdf4llm.to_markdown(temp_file.name)
#     return md_text

def pypdf2_extract(upload_file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(upload_file.file.read())
        # md_text = pymupdf4llm.to_markdown(temp_file.name)
        reader = PdfReader(temp_file.name)

        all_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                all_text += text

    return all_text


class FileValidationError(Exception):
    """Custom exception for file validation errors."""
    pass


def validate_pdf_file(upload_file: UploadFile) -> None:
    if not upload_file.filename.lower().endswith('.pdf'):
        raise FileValidationError("File is not a PDF.")

    if upload_file.size > settings.max_file_size:
        raise FileValidationError("File size exceeds 5 MB.")
