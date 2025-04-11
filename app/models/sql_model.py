from datetime import timezone
from typing import Optional, Dict, Any

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

from app.models.data_model import *


def JSONField(default_factory=dict):
    return Field(default_factory=default_factory, sa_column=Column(JSON))


class UserDocSQL(SQLModel, table=True):
    __tablename__ = "user_doc"

    user_id: str
    doc_id: Optional[int] = Field(default=None, primary_key=True)
    extracted_text: str
    upload_time: datetime


class UserDocBaseSQL(SQLModel, table=True):
    user_id: str
    doc_id: int = Field(default=None, primary_key=True)
    upload_time: datetime


class AttemptBaseSQL(SQLModel, table=True):
    attempt_id: Optional[int] = Field(default=None, primary_key=True)
    doc_id: int = Field(foreign_key="user_doc.doc_id")
    # doc_id: int
    attempt_num: int = Field(default=1)
    is_success: bool = Field(default=True)
    attempt_details: Dict[str, Any] = JSONField()  # JSON field
    attempt_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def get_attempt_data(self):
        return AttemptData(
            doc_id=self.doc_id,
            attempt_num=self.attempt_num,
            is_success=self.is_success,
            attempt_details=self.attempt_details,
            attempt_time=self.attempt_time
        )


class DocResultSQL(SQLModel, table=True):
    __tablename__ = "doc_result"

    user_id: str = Field(foreign_key="user_doc.user_id", primary_key=True)
    doc_id: int = Field(foreign_key="user_doc.doc_id", primary_key=True)

    mindmap: dict = JSONField()
    memory_tips: dict = JSONField()
    long_question: list[dict] = JSONField()
    flash_quiz: list[dict] = JSONField()


class LongQuestionSQL(SQLModel, table=True):
    __tablename__ = "long_questions"

    user_id: str
    doc_id: int = Field(foreign_key="user_doc.doc_id", primary_key=True)
    qid: int = Field(primary_key=True)
    question: str
    answer: str
