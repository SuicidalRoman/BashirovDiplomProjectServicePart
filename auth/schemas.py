
from fastapi_users import schemas
from Database.models import UserStatus


class UserRead(schemas.BaseUser[int]):
    id: int
    user_login: str
    user_status: UserStatus
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    user_login: str
    hashed_password: str
    user_status: UserStatus = UserStatus.CLIENT
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    user_login: str
    hashed_password: str
    user_status: UserStatus
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
