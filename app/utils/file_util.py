from fastapi import UploadFile
from configs.config import settings


class FileValidationError(Exception):
    """Custom exception for file validation errors."""
    pass

def validate_pdf_file(upload_file:UploadFile) -> None:
   
    if not upload_file.filename.lower().endswith('.pdf'):
        raise FileValidationError("File is not a PDF.")
    
    if upload_file.size > settings.max_file_size:
        raise FileValidationError("File size exceeds 5 MB.")