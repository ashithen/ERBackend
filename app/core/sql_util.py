from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


def init_sql_database():
    sqlite_url = "mysql+pymysql://data_admin@34.121.59.245:3306/doc_data"

    connect_args = {"check_same_thread": False}
    return create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


engine = init_sql_database()

SessionDep = Annotated[Session, Depends(get_session)]
