import sys
from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import API_V1_STR, OPENAPI_URL, PROJECT_NAME

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI(title=PROJECT_NAME, openapi_url=OPENAPI_URL)

app.include_router(api_router, prefix=API_V1_STR)
