import sys

from app.api.api_v1.api import api_router
from app.core.config import API_V1_STR, OPENAPI_URL, PROJECT_NAME
from app.db.session import Session
from fastapi import FastAPI
from starlette.requests import Request

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI(title=PROJECT_NAME, openapi_url=OPENAPI_URL)

app.include_router(api_router, prefix=API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response
