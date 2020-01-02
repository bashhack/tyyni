import pytest

from app import crud
from app.db.session import db_session
from app.db_models.user import User
from app.models.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_lower_string


@pytest.fixture
def user_setup():
    def _user_setup():
        email = random_lower_string()
        password = random_lower_string()
        return email, password

    return _user_setup


@pytest.fixture()
def create_user(user_setup):
    def _create_user():
        email, password = user_setup()
        user_in = UserCreate(email=email, password=password)
        user = crud.user.create_user(db_session, user_in=user_in)
        return user

    return _create_user


def test_create_user(user_setup):
    email, password = user_setup()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create_user(db_session, user_in=user_in)
    assert isinstance(user, User)
    assert user.email == email
    assert user.hashed_password == password


def test_get_users(create_user):
    user = create_user()
    users = crud.user.get_users(db_session)
    assert isinstance(users, list)
    assert user in users


def test_get_user_by_email(create_user):
    user = create_user()
    user_from_db = crud.user.get_user_by_email(db_session, user_email=user.email)
    assert user == user_from_db


def test_get_user_by_id(create_user):
    user = create_user()
    user_from_db = crud.user.get_user_by_id(db_session, user_id=user.id)
    assert user == user_from_db


def test_update_user(create_user):
    original_user = create_user()
    original_email_for_user = original_user.email
    user_in = UserUpdate(email="changed@email.com")
    user = crud.user.update_user(
        db_session, user_to_update=original_user, user_in=user_in
    )
    assert original_email_for_user != "changed@email.com"
    assert user == original_user
    assert user.email == "changed@email.com"
    assert original_user.email == "changed@email.com"


# def test_authenticated_user(create_user):
#     user = create_user()
#     authenticated_user = crud.user.authenticate(db_session, user_email=user.email)
#     assert authenticated_user
#     assert user.email == authenticated_user.email
#
#
# def test_non_authenticated_user(user_setup):
#     email, password = user_setup()
#     authenticated_user = crud.user.authenticate(db_session, user_email=email)
#     assert not authenticated_user
