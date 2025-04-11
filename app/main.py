import logging
import sys
from contextlib import asynccontextmanager

from asgi_correlation_id.middleware import CorrelationIdMiddleware
from fastapi import FastAPI, Request
from loguru import logger

from app.core.auth_util import init_firebase
from app.core.logger_util import InterceptHandler
from app.db.sql_util import SessionDep
from app.routers import docs

# logging
logger.remove()
logger.add(sys.stderr, format="{time} | {level} | {message}", level="INFO")
logger.add("logs/app.log", rotation="10 MB", level="DEBUG")
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_firebase()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(docs.router)

app.add_middleware(CorrelationIdMiddleware, header_name="X-Request-ID")

logger.info("FastAPI application is starting...")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.get("/")
async def root():
    return {"message": "Server is UP"}
