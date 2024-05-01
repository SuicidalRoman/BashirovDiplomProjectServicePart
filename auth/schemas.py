
from fastapi_users import schemas
from Database.models import UserStatus


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    user_status: UserStatus
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    user_status: UserStatus = UserStatus.CLIENT
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    email: str
    password: str
    user_status: UserStatus
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
