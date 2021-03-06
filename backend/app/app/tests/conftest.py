import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

import requests
from alembic import command
from alembic.config import Config
from app import crud
from app.core.config import (
    API_V1_STR,
    FIRST_SUPERUSER_EMAIL,
    FIRST_SUPERUSER_PASSWORD,
    SQLALCHEMY_DATABASE_URI,
)
from app.db.session import db_session
from app.main import app
from app.models.user import UserCreate
from app.tests.utils.utils import get_server_api
from starlette.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    url = SQLALCHEMY_DATABASE_URI
    create_engine(url)
    assert not database_exists(url), "Test database already exists. Aborting tests."
    create_database(url)  # Create the test database.
    config = Config("alembic.ini")  # Run the migrations.
    command.upgrade(config, "head")
    yield  # Run the tests.
    drop_database(url)  # Drop the test database.


@pytest.fixture
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """

    # TODO: Set headers here, to avoid having to set auth headers everywhere?

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def create_superuser(create_test_database):
    superuser = crud.user.get_user_by_email(
        db_session, user_email=FIRST_SUPERUSER_EMAIL
    )

    if not superuser:
        user_in = UserCreate(
            email=FIRST_SUPERUSER_EMAIL,
            password=FIRST_SUPERUSER_PASSWORD,
            is_active=True,
            is_superuser=True,
            full_name="Super User",
        )

        crud.user.create_user(db_session, user_in=user_in)


@pytest.fixture(scope="session", autouse=True)
def superuser_token_headers(create_superuser):
    server_api = get_server_api()
    form_data = {
        "username": FIRST_SUPERUSER_EMAIL,
        "password": FIRST_SUPERUSER_PASSWORD,
    }

    response = requests.post(
        f"{server_api}{API_V1_STR}/login/access-token", data=form_data
    )

    response_content = response.json()

    access_token = response_content.get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}

    return headers
