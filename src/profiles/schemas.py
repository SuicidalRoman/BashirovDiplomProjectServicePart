from pydantic import BaseModel
from datetime import datetime, date

from src.Database.models import ProfileType


class ProfileRead(BaseModel):
    id: int
    user_id: int
    registered_at: datetime
    updated_at: datetime
    profile_type: ProfileType
    surname: str
    firstname: str
    patronymic: str
    birthdate: date
    phone: str

class ProfileCreate(BaseModel):
    user_id: int
    registered_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    profile_type: ProfileType = ProfileType.INDIVIDUAL
    surname: str
    firstname: str
    patronymic: str
    birthdate: date
    phone: str

class ProfileUpdate(BaseModel):
    user_id: int
    updated_at: datetime = datetime.utcnow()
    profile_type: ProfileType = ProfileType.INDIVIDUAL
    surname: str
    firstname: str
    patronymic: str | None
    birthdate: date
    phone: str