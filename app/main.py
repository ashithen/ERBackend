from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, UploadFile

from app.core.auth_util import User_ID_Dep
from app.core.auth_util import init_firebase
from app.core.sql_util import SessionDep
from app.models.data_model import UserDocData
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


@app.get("/")
async def root(session : SessionDep):
    print(session)
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile, user_id: User_ID_Dep):
    validate_pdf_file(file)
    extracted_text = pypdf2_extract(file)
    # print(user_id)
    user_doc_data = UserDocData(user_id=user_id, extracted_text=extracted_text, upload_time=datetime.now())

    return {"filename": file.filename, "text": extracted_text, "user":user_id}
    
