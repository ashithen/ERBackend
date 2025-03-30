import tempfile

import pymupdf4llm
from fastapi import UploadFile


def extract_text_from_pdf(upload_file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(upload_file.file.read())
        md_text = pymupdf4llm.to_markdown(temp_file.name)
    return md_text

