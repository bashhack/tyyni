import random
import string

import requests
from app.core.config import (
    API_V1_STR,
    FIRST_SUPERUSER_EMAIL,
    FIRST_SUPERUSER_PASSWORD,
    SERVER_NAME,
)


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_server_api():
    server_name = f"http://{SERVER_NAME}"
    return server_name


def get_superuser_token_headers():
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
