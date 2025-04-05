from datetime import datetime

from pydantic import BaseModel


class UserDocData(BaseModel):
    user_id: str
    extracted_text: str
    upload_time: datetime

class DocResultData(BaseModel):
    user_id: str
    doc_id: int
    mind_map: dict
    memory: dict
    long_question: dict
    flash_quiz: dict

class LongQuestionData(BaseModel):
    qid: str
    question: str
    answer: str

class AttemptData:
    doc_id : int
    attempt_num : int
    is_success : bool
    attempt_details : dict
    attempt_time : datetime
