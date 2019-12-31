import requests
from app.core.config import API_V1_STR, FIRST_SUPERUSER_EMAIL, FIRST_SUPERUSER_PASSWORD
from app.tests.utils.utils import get_server_api
from starlette.status import HTTP_200_OK


def test_get_access_token():
    server_api = get_server_api()
    form_data = {
        "username": FIRST_SUPERUSER_EMAIL,
        "password": FIRST_SUPERUSER_PASSWORD,
    }

    response = requests.post(
        f"{server_api}{API_V1_STR}/login/access-token", data=form_data
    )

    response_content = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_content.get("access_token")


def test_use_access_token(superuser_token_headers):
    server_api = get_server_api()

    response = requests.post(
        f"{server_api}{API_V1_STR}/login/test-token", headers=superuser_token_headers
    )
    response_content = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_content.get("email")
