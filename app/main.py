from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, UploadFile
from app.core.auth_util import verify_and_get_user
from app.core.auth_util import init_firebase
from app.utils.file_util import validate_pdf_file
from app.utils.text_util import extract_text_from_pdf



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_firebase()
    yield

app = FastAPI(lifespan=lifespan, dependencies=[Depends(verify_and_get_user)])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    validate_pdf_file(file)
    extracted_text = extract_text_from_pdf(file)
    return {"filename": file.filename, "text": extracted_text}
    
