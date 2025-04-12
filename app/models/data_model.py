from datetime import datetime

from pydantic import BaseModel


class UserDocData(BaseModel):
    user_id: str
    doc_id: int | None = None
    extracted_text: str | None = None
    upload_time: datetime


class DocResultData(BaseModel):
    user_id: str
    doc_id: int
    mindmap: dict
    memory_tips: dict
    long_question: list[dict]
    flash_quiz: list[dict]

    class Config:
        extra = "ignore"


class LongQuestionData(BaseModel):
    user_id: str
    doc_id: int
    qid: int
    question: str
    answer: str


class AttemptData(BaseModel):
    doc_id: int
    attempt_num: int
    is_success: bool
    attempt_details: dict
    attempt_time: datetime


class UserDocWithAttemptsData(UserDocData):
    user_id: str
    doc_id: int
    extracted_text: str | None
    upload_time: datetime
    attempts: list[AttemptData]
