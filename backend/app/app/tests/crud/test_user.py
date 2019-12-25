import pytest

from app import crud
from app.db.session import db_session
from app.db_models.user import User
from app.models.user import UserCreate
from app.tests.utils.utils import random_lower_string


@pytest.fixture
def user_setup():
    email = random_lower_string()
    password = random_lower_string()
    return email, password


@pytest.fixture
def create_user(user_setup):
    email, password = user_setup
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create_user(db_session, user_in=user_in)
    return user


def test_create_user(user_setup):
    email, password = user_setup
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create_user(db_session, user_in=user_in)
    assert isinstance(user, User)
    assert user.email == email
    assert user.hashed_password == password


def test_get_users(create_user):
    user = create_user
    users = crud.user.get_users(db_session)
    assert isinstance(users, list)
    assert user in users


def test_get_user_by_email(create_user):
    user = create_user
    user_from_db = crud.user.get_user_by_email(db_session, user_email=user.email)
    assert user == user_from_db
