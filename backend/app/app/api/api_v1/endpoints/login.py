from datetime import timedelta

from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.jwt import create_access_token
from app.db_models.user import User as DBUser
from app.models.token import Token
from app.models.user import User
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# TODO: Add support for third-party provider login via Google/Faceboook: https://docs.authlib.org/en/latest/client/starlette.html
# TODO: Keep an eye on this PR for authorization_code support: https://github.com/tiangolo/fastapi/pull/797/files


@router.post("/login/access-token", response_model=Token, tags=["Login"])
def login_access_token(
    db_session: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """

    NOTE:
        Using the dependency class `OAuth2PasswordRequestForm`
        creates the following Form request parameters for the endpoint:

        - grant_type: the OAuth2 spec says it is required and MUST be the fixed string "password".
          Nevertheless, this dependency class is permissive and allows not passing it.
          If you want to enforce it, use instead the OAuth2PasswordRequestFormStrict dependency.
        - username: username string.
          The OAuth2 spec requires the exact field name "username".
        - password: password string.
          The OAuth2 spec requires the exact field name "password".
        - scope: Optional string.
          Several scopes (each one a string) separated by spaces.
          E.g. "items:read items:write users:read profile openid"
        - client_id: optional string.
          OAuth2 recommends sending the client_id and client_secret (if any)
          using HTTP Basic auth, as: client_id:client_secret
        - client_secret: optional string.
          OAuth2 recommends sending the client_id and client_secret (if any)
          using HTTP Basic auth, as: client_id:client_secret

    """

    user = crud.user.authenticate(db_session, user_email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            payload={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", tags=["Login"], response_model=User)
def test_token(current_user: DBUser = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user
