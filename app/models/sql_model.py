from datetime import timezone
from typing import Optional, Dict, Any

from sqlmodel import SQLModel, Field, Relationship

from app.models.data_model import *


class UserDocBaseSQL(SQLModel, table=True):
    user_id: str = Field(foreign_key="user_doc.user_id", max_length=255)
    doc_id: Optional[int] = Field(default=None, primary_key=True)
    extracted_text: str
    upload_time: datetime

    @classmethod
    def from_user_doc_data(cls, user_doc_data:UserDocData):
        return cls(
            user_id=user_doc_data.user_id,
            extracted_text=user_doc_data.extracted_text,
            upload_time=user_doc_data.upload_time
        )

    def get_user_doc_data(self) -> UserDocData:
        return UserDocData(
            user_id=self.user_id,
            doc_id=self.doc_id,
            extracted_text=self.extracted_text,
            upload_time=self.upload_time
        )


class UserDocExtendedSQL(SQLModel, table=True):
    user_id: str = Field(foreign_key="user_doc.user_id", max_length=255)
    doc_id: Optional[int] = Field(default=None, primary_key=True)
    upload_time: datetime
    # Relationships
    attempts: list["AttemptBaseSQL"] = Relationship(back_populates="user_doc")
    # doc_result: list["DocResult"] = Relationship(back_populates="user_doc")

    def get_user_data_with_attempts(self) -> UserDocWithAttemptsData:
        attempts_data = [
            attempt.get_attempt_data() for attempt in self.attempts
        ]
        return UserDocWithAttemptsData(
            user_id=self.user_id,
            doc_id=self.doc_id,
            extracted_text=None,
            upload_time=self.upload_time,
            attempts=attempts_data
        )





class AttemptBaseSQL(SQLModel, table=True):
    attempt_id: Optional[int] = Field(default=None, primary_key=True)
    doc_id: int = Field(foreign_key="user_doc.doc_id")
    attempt_num: int = Field(default=1)
    is_success: bool = Field(default=True)
    attempt_details: Dict[str, Any]  # JSON field
    attempt_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    # user_doc: Optional[UserDoc] = Relationship(back_populates="attempts")

    def get_attempt_data(self):
        return AttemptData(
            doc_id=self.doc_id,
            attempt_num=self.attempt_num,
            is_success=self.is_success,
            attempt_details=self.attempt_details,
            attempt_time=self.attempt_time
        )


class DocResultBaseSQL(SQLModel, table=True):
    user_id: str = Field(foreign_key="user_doc.user_id", primary_key=True)
    doc_id: int = Field(foreign_key="user_doc.doc_id", primary_key=True)

    mind_map: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)
    long_question: Dict[str, Any] = Field(default_factory=dict)
    flash_quiz: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_doc_result_data(cls, doc_result_data: DocResultData):
        return cls(
            user_id=doc_result_data.user_id,
            doc_id=doc_result_data.doc_id,
            mind_map=doc_result_data.mind_map,
            memory=doc_result_data.memory,
            long_question=doc_result_data.long_question,
            flash_quiz=doc_result_data.flash_quiz
        )


    # Relationships
    # user_doc: Optional[UserDoc] = Relationship(back_populates="doc_result")


class LongQuestionSQL(SQLModel, table=True):
    doc_id: int = Field(foreign_key="user_doc.doc_id", primary_key=True)
    qid: int = Field(primary_key=True)
    question: str
    answer: str

    @classmethod
    def from_long_question_data(cls, long_question_data: LongQuestionData):
        return cls(
            doc_id=long_question_data.doc_id,
            qid=long_question_data.qid,
            question=long_question_data.question,
            answer=long_question_data.answer
        )

