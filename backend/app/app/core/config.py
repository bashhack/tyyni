from decouple import config

API_V1 = "/api/v1"

PROJECT_NAME = config("PROJECT_NAME", default=None)
API_V1_STR = config("API_V1_STR", default=API_V1)
OPENAPI_URL = config("OPENAPI_URL", default=f"{API_V1}/openapi.json")
