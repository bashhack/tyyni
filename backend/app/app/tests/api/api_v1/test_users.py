import pytest

from app import crud
from app.core.config import API_V1_STR
from app.db.session import db_session
from app.models.user import UserCreate, UserUpdate
from app.tests.utils.utils import get_server_api, random_lower_string
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


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


def test_create_user(client, user_setup, superuser_token_headers):
    server_api = get_server_api()
    email, password = user_setup()

    user_in = UserCreate(email=email, password=password, full_name="Foo Bar")

    request = {
        "email": user_in.email,
        "is_active": True,
        "is_superuser": False,
        "full_name": user_in.full_name,
        "password": "string",
    }

    response = client.post(
        f"{server_api}{API_V1_STR}/users/",
        json=request,
        headers=superuser_token_headers,
    )

    response_content = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_content.get("email") == user_in.email
    assert response_content.get("password") is None


def test_creating_user_with_existing_credentials_returns_error(
    client, create_user, superuser_token_headers
):
    server_api = get_server_api()
    user = create_user()

    request = {
        "email": user.email,
        "is_active": True,
        "is_superuser": False,
        "full_name": user.full_name,
        "password": "string",
    }

    response = client.post(
        f"{server_api}{API_V1_STR}/users/",
        json=request,
        headers=superuser_token_headers,
    )

    response_content = response.json()

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert (
        response_content.get("message")
        == f"A user already exists with username: {user.email}"
    )


def test_get_users(client, create_user, superuser_token_headers):
    server_api = get_server_api()
    user = create_user()
    other_user = create_user()

    assert user.email != other_user.email

    response = client.get(
        f"{server_api}{API_V1_STR}/users/", headers=superuser_token_headers
    )

    response_content = response.json()

    assert response.status_code == HTTP_200_OK
    assert len(response_content) > 1

    for user in response_content:
        assert "email" in user


# @pytest.mark.parametrize("status_code", [(HTTP_200_OK,), (HTTP_404_NOT_FOUND,)])
# def test_get_user(client, create_user, status_code, superuser_token_headers):
#     server_api = get_server_api()
#     user = create_user()
#
#     if status_code == HTTP_200_OK:
#         user_id = user.id
#     else:
#         user_id = 0
#
#     response = client.get(
#         f"{server_api}{API_V1_STR}/users/{user_id}", headers=superuser_token_headers
#     )
#
#     response_content = response.json()
#
#     if status_code == HTTP_200_OK:
#         assert response.status_code == HTTP_200_OK
#
#         assert response_content.get("email") == user.email
#     else:
#         assert response.status_code == HTTP_404_NOT_FOUND
#
#         assert (
#             response_content.get("message") == f"No user found with user_id: {user_id}"
#         )
#
#     assert db_session.query(User).count() == 2


def test_get_user(client, create_user, superuser_token_headers):
    server_api = get_server_api()
    user = create_user()

    response = client.get(
        f"{server_api}{API_V1_STR}/users/{user.id}", headers=superuser_token_headers
    )

    response_content = response.json()

    assert response.status_code == HTTP_200_OK

    assert response_content.get("email") == user.email


def test_get_user_returns_404_if_user_not_found(client, superuser_token_headers):
    server_api = get_server_api()

    user_id = 0

    response = client.get(
        f"{server_api}{API_V1_STR}/users/{user_id}", headers=superuser_token_headers
    )

    response_content = response.json()

    assert response.status_code == HTTP_404_NOT_FOUND

    assert response_content.get("message") == f"No user found with user_id: {user_id}"


# @pytest.mark.parametrize("status_code", [(HTTP_200_OK,), (HTTP_404_NOT_FOUND,)])
# def test_update_user(client, create_user, status_code, superuser_token_headers):
#     server_api = get_server_api()
#     user = create_user()
#     original_user_email = user.email
#
#     if status_code == HTTP_200_OK:
#         user_id = user.id
#     else:
#         user_id = 0
#
#     user_in = UserUpdate(email="changed@email.com")
#
#     request = {"email": user_in.email, "password": "changed_password"}
#
#     response = client.put(
#         f"{server_api}{API_V1_STR}/users/{user_id}",
#         json=request,
#         headers=superuser_token_headers,
#     )
#
#     response_content = response.json()
#
#     if status_code == HTTP_200_OK:
#         assert response.status_code == HTTP_200_OK
#         assert response_content.get("id") == user.id
#         assert original_user_email != "changed@email.com"
#         assert response_content.get("email") == "changed@email.com"
#     else:
#         assert response.status_code == HTTP_404_NOT_FOUND
#
#         assert (
#             response_content.get("message") == f"No user found with user_id: {user_id}"
#         )


def test_update_user(client, create_user, superuser_token_headers):
    server_api = get_server_api()
    user = create_user()
    original_user_email = user.email

    user_in = UserUpdate(email="changed@email.com")

    request = {"email": user_in.email, "password": "changed_password"}

    response = client.put(
        f"{server_api}{API_V1_STR}/users/{user.id}",
        json=request,
        headers=superuser_token_headers,
    )

    response_content = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_content.get("id") == user.id
    assert original_user_email != "changed@email.com"
    assert response_content.get("email") == "changed@email.com"


def test_update_user_returns_404_if_user_not_found(client, superuser_token_headers):
    server_api = get_server_api()

    user_id = 0

    user_in = UserUpdate(email="changed@email.com")

    request = {"email": user_in.email, "password": "changed_password"}

    response = client.put(
        f"{server_api}{API_V1_STR}/users/{user_id}",
        json=request,
        headers=superuser_token_headers,
    )

    response_content = response.json()

    assert response.status_code == HTTP_404_NOT_FOUND

    assert response_content.get("message") == f"No user found with user_id: {user_id}"
