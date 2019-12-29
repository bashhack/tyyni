import pytest
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from app import crud
from app.core.config import API_V1_STR
from app.db.session import db_session
from app.models.user import UserCreate
from app.tests.utils.utils import get_server_api, random_lower_string


@pytest.fixture
def user_setup():
    def _user_setup():
        email = random_lower_string()
        password = random_lower_string()
        return email, password

    return _user_setup


@pytest.fixture
def create_user(user_setup):
    def _create_user():
        email, password = user_setup()
        user_in = UserCreate(email=email, password=password)
        user = crud.user.create_user(db_session, user_in=user_in)
        return user

    return _create_user


def test_get_users(client, create_user):
    server_api = get_server_api()
    user = create_user()
    other_user = create_user()
    assert user.email != other_user.email

    response = client.get(f"{server_api}{API_V1_STR}/users/")

    users_from_req = response.json()

    assert response.status_code == HTTP_200_OK

    assert len(users_from_req) > 1
    for user in users_from_req:
        assert "email" in user


@pytest.mark.parametrize("status_code", [(HTTP_200_OK,), (HTTP_404_NOT_FOUND,)])
def test_get_user(client, create_user, status_code):
    server_api = get_server_api()
    user = create_user()

    if status_code == HTTP_200_OK:
        user_id = user.id
    else:
        user_id = 0

    response = client.get(f"{server_api}{API_V1_STR}/users/{user_id}")

    user_from_req = response.json()

    if status_code == HTTP_200_OK:
        assert response.status_code == HTTP_200_OK

        assert user_from_req.get("email") == user.email
    else:
        assert response.status_code == HTTP_404_NOT_FOUND
