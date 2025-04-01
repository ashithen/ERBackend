import tempfile

import pymupdf4llm
from fastapi import UploadFile
from PyPDF2 import PdfReader

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
