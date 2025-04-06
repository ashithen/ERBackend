from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.core.config import settings


def init_sql_database():
    sqlite_url = (
        f"mysql+pymysql://{settings.sql_username}@{settings.sql_address}:{settings.sql_port}/{settings.sql_database}"
    )

    connect_args = {"check_same_thread": False}
    return create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


engine = init_sql_database()

SessionDep = Annotated[Session, Depends(get_session)]
