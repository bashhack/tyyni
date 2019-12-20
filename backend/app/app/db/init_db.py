from app.core.config import FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD
from app.crud.user import create_user, get_user_by_email
from app.db.session import Session
from app.models.user import UserCreate


def init_db(db_session: Session) -> None:
    user = get_user_by_email(db_session, email=FIRST_SUPERUSER)

    if not user:
        user_in = UserCreate(
            email=FIRST_SUPERUSER, password=FIRST_SUPERUSER_PASSWORD, is_superuser=True
        )
        create_user(db_session, user_in=user_in)
