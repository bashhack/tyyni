from decouple import config

API_V1 = "/api/v1"

PROJECT_NAME = config("PROJECT_NAME", default=None)
API_V1_STR = config("API_V1_STR", default=API_V1)
OPENAPI_URL = config("OPENAPI_URL", default=f"{API_V1}/openapi.json")

POSTGRES_USER = config("POSTGRES_USER", default=None)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", default=None)
POSTGRES_SERVER = config("POSTGRES_SERVER", default=None)
POSTGRES_DB = config("POSTGRES_DB", default=None)
SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
