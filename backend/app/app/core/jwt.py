from datetime import timedelta, datetime

import jwt

from app.core.config import SECRET_KEY

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

def create_access_token(*, payload: dict, expires_delta: timedelta = None):
    to_encode = payload.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({
        "exp": expire, "sub": access_token_jwt_subject
    })

    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt