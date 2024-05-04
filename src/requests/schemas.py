from pydantic import BaseModel
from datetime import datetime

from src.Database.models import EventType

class RequestRead(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    request_title: str
    event_title: str
    event_type: EventType

class RequestCreate(BaseModel):
    user_id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    request_title: str
    event_title: str
    event_type: EventType = EventType.CONFERENCE

class RequestUpdate(BaseModel):
    id: int
    updated_at: datetime = datetime.utcnow()
    request_title: str
    event_title: str
    event_type: EventType

