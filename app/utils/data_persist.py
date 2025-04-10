from app.core.sql_util import get_session
from app.models.sql_model import *


async def save_user_doc(user_doc_data: UserDocData) -> int:
    used_doc_sql = UserDocBaseSQL.from_user_doc_data(user_doc_data)
    with get_session() as session:
        session.add(used_doc_sql)
        session.commit()
        session.refresh(used_doc_sql)
        return used_doc_sql.doc_id


async def save_doc_result(user_doc_result: DocResultData):
    doc_result_sql = DocResultBaseSQL.from_doc_result_data(user_doc_result)
    with get_session() as session:
        session.add(doc_result_sql)
        session.commit()


async def save_long_questions(long_questions: list[LongQuestionData]):
    with get_session() as session:
        for long_question in long_questions:
            long_question_sql = LongQuestionSQL.from_long_question_data(long_question)
            session.add(long_question_sql)
        session.commit()


def get_user_all_doc_minimal(user_id: str) -> list[UserDocWithAttemptsData]:
    with get_session() as session:
        user_docs = session.query(UserDocExtendedSQL).filter(UserDocExtendedSQL.user_id == user_id).all()
        return [doc.get_user_data_with_attempts() for doc in user_docs]


def get_mindmap_for(user_id: str, doc_id: int) -> dict:
    with get_session() as session:
        mindmap = session.query(DocResultBaseSQL.mind_map).filter(DocResultBaseSQL.user_id == user_id,
                                                                  DocResultBaseSQL.doc_id == doc_id).first
        return mindmap


def get_long_questions_for(user_id: str, doc_id: int) -> dict:
    with get_session() as session:
        long_questions = session.query(DocResultBaseSQL.long_question).filter(DocResultBaseSQL.user_id == user_id,
                                                                              DocResultBaseSQL.doc_id == doc_id).first
        return long_questions


def get_flash_quiz_for(user_id: str, doc_id: int) -> dict:
    with get_session() as session:
        flash_quiz = session.query(DocResultBaseSQL.flash_quiz).filter(DocResultBaseSQL.user_id == user_id,
                                                                       DocResultBaseSQL.doc_id == doc_id).first
        return flash_quiz


def get_memory_for(user_id: str, doc_id: int) -> dict:
    with get_session() as session:
        memory = session.query(DocResultBaseSQL.memory).filter(DocResultBaseSQL.user_id == user_id,
                                                               DocResultBaseSQL.doc_id == doc_id).first
        return memory


def delete_doc(user_id: str, doc_id: int):
    with get_session() as session:
        user_doc = session.query(UserDocBaseSQL).filter(UserDocBaseSQL.user_id == user_id,
                                                        UserDocBaseSQL.doc_id == doc_id).first()
        if not user_doc:
            raise Exception("No such document found for given user")
        session.delete(user_doc)
        doc_result = session.query(DocResultBaseSQL).filter(DocResultBaseSQL.user_id == user_id,
                                                            DocResultBaseSQL.doc_id == doc_id).first()
        if doc_result:
            session.delete(doc_result)
        all_attempts = session.query(AttemptBaseSQL).filter(AttemptBaseSQL.doc_id == doc_id).all()
        for attempt in all_attempts:
            session.delete(attempt)
        all_questions = session.query(LongQuestionSQL).fiter(LongQuestionSQL.doc_id == doc_id).all()
        for question in all_questions:
            session.delete(question)
        session.commit()
