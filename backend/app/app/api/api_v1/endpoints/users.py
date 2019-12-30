from typing import List

from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.error_handlers import (
    ErrorMessage,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.models.user import User, UserCreate
from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

router = APIRouter()


@router.get("/", response_model=List[User])
def get_users(db_session: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """ Get a list of users """

    users = crud.user.get_users(db_session, skip=skip, limit=limit)
    return users


@router.post(
    "/",
    response_model=User,
    status_code=HTTP_201_CREATED,
    responses={HTTP_400_BAD_REQUEST: {"model": ErrorMessage}},
)
def create_user(*, db_session: Session = Depends(get_db), user_in: UserCreate):
    """ Create a new user """

    user = crud.user.get_user_by_email(db_session=db_session, user_email=user_in.email)
    if user:
        # TODO: Feeling uneasy about this whole approach - probably want to switch over
        #       to a 200_OK + notification email solution to avoid enumeration attacks.
        #       ...
        #       I think I might want to instead rely on a notification email system,
        #       so that if a request to create a new user account is made:
        #       ...
        #       1. User enters their alleged email.
        #       2. An email is sent to that address, containing a one-time registration link;
        #          however, if the email is already registered, then an email is sent explaining that fact.
        #          No clue is revealed in the response to the original request as to whether the email already existed in the system or not.
        #       3. The user registers by following the link from the email.

        raise UserAlreadyExistsException(username=user_in.email)
    user = crud.user.create_user(db_session=db_session, user_in=user_in)
    return user


@router.get(
    "/{user_id}",
    response_model=User,
    responses={HTTP_404_NOT_FOUND: {"model": ErrorMessage}},
)
def get_user(*, db_session: Session = Depends(get_db), user_id: int):
    """ Get a user by user ID """

    user = crud.user.get_user_by_id(db_session=db_session, user_id=user_id)
    # TODO: Raise a 403 Unauthorized, here? Not everyone should have access...
    if not user:
        raise UserNotFoundException(user_id=user_id)
    return user
