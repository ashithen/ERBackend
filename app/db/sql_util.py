import urllib
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.core.config import settings


def init_sql_database():
    pwd = urllib.parse.quote_plus(settings.sql_password)
    sqlite_url = (
        f"mysql+pymysql://{settings.sql_username}:{pwd}@{settings.sql_address}:{settings.sql_port}/{settings.sql_database}"
    )
    return create_engine(sqlite_url)


def get_session():
    with Session(engine) as session:
        yield session


engine = init_sql_database()

SessionDep = Annotated[Session, Depends(get_session)]
