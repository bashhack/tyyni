from app.api.api_v1.endpoints import users
from fastapi.routing import APIRouter

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Users"])
