from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app import crud
from app.api.utils.db import get_db
from app.models.user import User, UserCreate

router = APIRouter()


@router.get("/", response_model=List[User])
def get_users(db_session: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """ Get a list of users """

    users = crud.user.get_users(db_session, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
def create_user(*, db_session: Session = Depends(get_db), user_in: UserCreate):
    """ Create a new user """

    user = crud.user.get_user_by_email(db_session=db_session, user_email=user_in.email)
    if user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists.",
        )
    user = crud.user.create_user(db_session=db_session, user_in=user_in)
    return user
