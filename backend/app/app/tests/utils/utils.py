import random
import string

from app.core.config import SERVER_NAME


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_server_api():
    server_name = f"http://{SERVER_NAME}"
    return server_name
