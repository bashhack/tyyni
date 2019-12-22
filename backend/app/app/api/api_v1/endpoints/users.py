from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.models.user import User, UserCreate

router = APIRouter()


@router.get("/", response_model=List[User])
def get_users(db_session: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    users = crud.user.get_users(db_session, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
def create_user(*, db_session: Session = Depends(get_db), user_in: UserCreate):
    user = "foo"
    return user
