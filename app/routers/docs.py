import asyncio
from datetime import datetime

from fastapi import APIRouter
from fastapi import UploadFile

from app.core.auth_util import User_ID_Dep
from app.db.data_persist import save_all_results
from app.db.data_persist import save_user_doc
from app.db.sql_util import SessionDep
from app.models.data_model import UserDocData, DocResultData, LongQuestionData
from app.utils.llm_util import generate_doc_result
from app.utils.pdf_util import pypdf2_extract, validate_pdf_file

router = APIRouter()


@router.post("/uploadfile/")
async def upload_file(file: UploadFile, user_id: User_ID_Dep, session: SessionDep):
    validate_pdf_file(file)
    extracted_text = pypdf2_extract(file)
    user_doc_data = UserDocData(user_id=user_id, extracted_text=extracted_text, upload_time=datetime.now())
    doc_id, doc_res_dict = await asyncio.gather(save_user_doc(user_doc_data, session),
                                                generate_doc_result(extracted_text))
    user_doc_data.doc_id = doc_id
    doc_result_data, long_questions = process_doc_result(user_doc_data, doc_res_dict)
    await save_all_results(doc_result_data, long_questions, session)

    return {"filename": file.filename, "user": user_id, "doc_id": doc_id}


def process_doc_result(user_doc_data: UserDocData, doc_res_dict: dict) -> (DocResultData, [LongQuestionData]):
    long_questions = []
    long_question_data_list: list[LongQuestionData] = []
    for i, qa_dict in enumerate(doc_res_dict["long_answer_questions"]):
        long_questions.append({i: qa_dict['question']})
        long_question_data_list.append(
            LongQuestionData(user_id=user_doc_data.user_id, doc_id=user_doc_data.doc_id, qid=i,
                             question=qa_dict['question'],
                             answer=qa_dict['answer']))
    return (DocResultData(user_id=user_doc_data.user_id, doc_id=user_doc_data.doc_id,
                          long_question=long_questions,
                          **doc_res_dict), long_question_data_list)
