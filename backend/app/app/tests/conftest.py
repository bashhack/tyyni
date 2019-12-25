import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from starlette.testclient import TestClient

from app.main import app

# IMPORTANT: Need to set this before attempting to import the DB URI!!!
os.environ["TESTING"] = "True"

from app.core.config import SQLALCHEMY_DATABASE_URI


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


@pytest.fixture()
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    with TestClient(app) as client:
        yield client
