from sqlalchemy.orm import Session

from app.core.config import FIRST_SUPERUSER_EMAIL, FIRST_SUPERUSER_PASSWORD
from app.crud.user import create_user, get_user_by_email
from app.models.user import UserCreate


def init_db(db_session: Session) -> None:
    user = get_user_by_email(db_session, user_email=FIRST_SUPERUSER_EMAIL)

    if not user:
        user_in = UserCreate(
            email=FIRST_SUPERUSER_EMAIL,
            password=FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        create_user(db_session, user_in=user_in)
