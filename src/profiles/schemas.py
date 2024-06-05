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

    class Config:
        orm_mode = True
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ProfileCreate(BaseModel):
    user_id: int
    profile_type: ProfileType = ProfileType.INDIVIDUAL
    surname: str
    firstname: str
    patronymic: str
    birthdate: date
    phone: str

class ProfileUpdate(BaseModel):
    profile_type: ProfileType = ProfileType.INDIVIDUAL
    surname: str
    firstname: str
    patronymic: str | None
    birthdate: date
    phone: str
