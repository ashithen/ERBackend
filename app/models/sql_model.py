from typing import Optional, Dict, Any
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, JSON


class UserDocBaseSQL(SQLModel, table=True):
    user_id: str = Field(foreign_key="user_doc.user_id", max_length=255)
    doc_id: Optional[int] = Field(default=None, primary_key=True)
    extracted_text: str
    upload_time: datetime

class UserDocExtendedSQL(UserDocBaseSQL, table=True):
    # Relationships
    attempts: list["AttemptBaseSQL"] = Relationship(back_populates="user_doc")
    # doc_result: list["DocResult"] = Relationship(back_populates="user_doc")


class AttemptBaseSQL(SQLModel, table=True):
    attempt_id: Optional[int] = Field(default=None, primary_key=True)
    doc_id: int = Field(foreign_key="user_doc.doc_id")
    attempt_num: int = Field(default=1)
    is_success: bool = Field(default=True)
    attempt_details: Dict[str, Any]  # JSON field
    attempt_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    # user_doc: Optional[UserDoc] = Relationship(back_populates="attempts")


class DocResultBaseSQL(SQLModel, table=True):
    user_id: str = Field(foreign_key="user_doc.user_id", primary_key=True)
    doc_id: int = Field(foreign_key="user_doc.doc_id", primary_key=True)

    mind_map: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)
    long_question: Dict[str, Any] = Field(default_factory=dict)
    flash_quiz: Dict[str, Any] = Field(default_factory=dict)

    # Relationships
    # user_doc: Optional[UserDoc] = Relationship(back_populates="doc_result")


class LongQuestion(SQLModel, table=True):
    qid: str = Field(primary_key=True, max_length=255)
    question: str
    answer: str
