import sys

from app.core import config
from fastapi import FastAPI

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI(title=config.PROJECT_NAME, openapi_url=config.OPENAPI_URL)
