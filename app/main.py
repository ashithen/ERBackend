from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, UploadFile, Header
from app.core.auth_util import verify_and_get_user
from app.core.auth_util import init_firebase
from app.utils.file_util import validate_pdf_file
# from app.utils.text_util import extract_text_from_pdf
from app.utils.text_util import pypdf2_extract



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_firebase()
    yield

app = FastAPI(lifespan=lifespan,
              # dependencies=[Depends(verify_and_get_user)]
              )
User_ID_Dep = Annotated[str, Depends(verify_and_get_user)]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile, user_id: User_ID_Dep):
    validate_pdf_file(file)
    extracted_text = pypdf2_extract(file)

    return {"filename": file.filename, "text": extracted_text, "user":user_id}
    
