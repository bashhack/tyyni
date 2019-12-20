from app.db.session import Session
from app.db_models.user import User
from app.models.user import UserCreate


def get_user_by_email(db_session: Session, *, email: str):
    return db_session.query(User).filter(User.email == email).first()


def create_user(db_session: Session, *, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        hashed_password=user_in.password,
        full_name=user_in.full_name,
        is_superuser=user_in.is_superuser,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
