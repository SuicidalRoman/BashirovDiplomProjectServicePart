from pydantic import BaseModel
from datetime import datetime
from src.Database.models import EventType

class EventRead(BaseModel):
    id: int
    request_id: int
    title: str
    description: str | None
    event_type: EventType
    start_timestamp: datetime
    end_timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EventCreate(BaseModel):
    request_id: int
    title: str
    description: str | None
    event_type: EventType = EventType.CONFERENCE
    start_timestamp: datetime
    end_timestamp: datetime

class EventUpdate(BaseModel):
    id: int
    title: str
    description: str | None
    event_type: EventType
    start_timestamp: datetime
    end_timestamp: datetime
