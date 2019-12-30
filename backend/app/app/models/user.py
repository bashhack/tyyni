from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None

    class Config:
        orm_mode = True


class UserBaseInDB(UserBase):
    id: int = None


class User(UserBaseInDB):
    pass


class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


class UserCreate(UserBase):
    email: str
    password: str
