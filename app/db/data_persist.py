from sqlmodel import Session

from app.models.sql_model import *


async def save_user_doc(user_doc_data: UserDocData, session: Session) -> int:
    used_doc_sql = UserDocSQL.model_validate(user_doc_data)
    session.add(used_doc_sql)
    session.commit()
    session.refresh(used_doc_sql)
    return used_doc_sql.doc_id


async def save_doc_result(user_doc_result: DocResultData, session: Session):
    doc_result_sql = DocResultSQL.from_doc_result_data(user_doc_result)
    session.add(doc_result_sql)
    session.commit()


async def save_long_questions(long_questions: list[LongQuestionData], session: Session):
    for long_question in long_questions:
        long_question_sql = LongQuestionSQL.from_long_question_data(long_question)
        session.add(long_question_sql)
    session.commit()


async def save_all_results(user_doc_result: DocResultData, long_questions: list[LongQuestionData], session: Session):
    doc_result_sql = DocResultSQL.model_validate(user_doc_result)
    session.add(doc_result_sql)
    for long_question in long_questions:
        long_question_sql = LongQuestionSQL.model_validate(long_question)
        session.add(long_question_sql)
    session.commit()


def get_mindmap_for(user_id: str, doc_id: int, session: Session) -> dict:
    mindmap = session.query(DocResultSQL.mindmap).filter(DocResultSQL.user_id == user_id,
                                                         DocResultSQL.doc_id == doc_id).first
    return mindmap


def get_long_questions_for(user_id: str, doc_id: int, session: Session) -> dict:
    long_questions = session.query(DocResultSQL.long_question).filter(DocResultSQL.user_id == user_id,
                                                                      DocResultSQL.doc_id == doc_id).first
    return long_questions


def get_flash_quiz_for(user_id: str, doc_id: int, session: Session) -> dict:
    flash_quiz = session.query(DocResultSQL.flash_quiz).filter(DocResultSQL.user_id == user_id,
                                                               DocResultSQL.doc_id == doc_id).first
    return flash_quiz


def get_memory_for(user_id: str, doc_id: int, session: Session) -> dict:
    memory = session.query(DocResultSQL.memory_tips).filter(DocResultSQL.user_id == user_id,
                                                            DocResultSQL.doc_id == doc_id).first
    return memory

# def delete_doc(user_id: str, doc_id: int, session: Session):
#     user_doc = session.query(UserDocSQL).filter(UserDocCreateSQL.user_id == user_id,
#                                                       UserDocCreateSQL.doc_id == doc_id).first()
#     if not user_doc:
#         raise Exception("No such document found for given user")
#     session.delete(user_doc)
#     doc_result = session.query(DocResultSQL).filter(DocResultSQL.user_id == user_id,
#                                                     DocResultSQL.doc_id == doc_id).first()
#     if doc_result:
#         session.delete(doc_result)
#     all_attempts = session.query(AttemptBaseSQL).filter(AttemptBaseSQL.doc_id == doc_id).all()
#     for attempt in all_attempts:
#         session.delete(attempt)
#     all_questions = session.query(LongQuestionSQL).fiter(LongQuestionSQL.doc_id == doc_id).all()
#     for question in all_questions:
#         session.delete(question)
#     session.commit()
