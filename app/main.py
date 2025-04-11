from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.auth_util import init_firebase
from app.db.sql_util import SessionDep
from app.routers import docs


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_firebase()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(docs.router)


@app.get("/")
async def root(session: SessionDep):
    print(session)
    return {"message": "Hello World"}
