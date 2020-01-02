import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.error_handlers import UserNotFoundException
from app.core.config import SECRET_KEY
from app.core.jwt import ALGORITHM
from app.db_models.user import User
from app.models.token import TokenPayload
from fastapi import HTTPException
from fastapi.params import Depends, Security
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


def get_current_user(
    db_session: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    user_id = token_data.user_id
    user = crud.user.get_user_by_id(db_session=db_session, user_id=user_id)

    if not user:
        raise UserNotFoundException(user_id=user_id)

    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
