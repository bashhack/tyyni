import sys

from app.api.api_v1.api import api_router
from app.api.utils.error_handlers import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.core.config import API_V1_STR, OPENAPI_URL, PROJECT_NAME
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI(title=PROJECT_NAME, openapi_url=OPENAPI_URL)

app.include_router(api_router, prefix=API_V1_STR)


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content={"message": f"No user found with user_id: {exc.user_id}"},
    )


@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsException
):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"message": f"A user already exists with username: {exc.username}"},
    )
