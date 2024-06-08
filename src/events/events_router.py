from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, insert, text
from datetime import datetime
from typing import List
from src.auth.database import get_async_session, User
from src.Database.models import events
from src.events.schemas import EventCreate, EventRead, EventUpdate
from src.auth.manager import current_user

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("/", response_model=List[EventRead])
@cache(expire=60)
async def get_all_events(session: AsyncSession = Depends(get_async_session)):
    query = select(events)
    result = await session.execute(query)
    events_data = result.fetchall()
    
    events_dicts = [
        dict(zip(result.keys(), event_tuple)) for event_tuple in events_data
    ]
    
    return [EventRead(**event_dict) for event_dict in events_dicts]


@router.get("/{event_id}", response_model=EventRead)
@cache(expire=60)
async def get_specific_event(event_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(events).where(events.c.event_id == event_id)
    result = await session.execute(query)
    event_data = result.first()

    if not event_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    event_dict = dict(zip(result.keys(), event_data))
    event_dict["id"] = event_dict.pop("event_id")

    return EventRead(**event_dict)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventRead)
async def create_new_event(
    new_event: EventCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    new_event_data = new_event.dict()
    # new_event_data["created_at"] = text('NOW()')
    # new_event_data["updated_at"] = text('NOW()')
    statement = insert(events).values(**new_event_data).returning(events)
    result = await session.execute(statement)
    await session.commit()
    created_event = result.first()

    if not created_event:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event could not be created")

    created_event_dict = dict(zip(result.keys(), created_event))
    created_event_dict["id"] = created_event_dict.pop("event_id")

    return EventRead(**created_event_dict)

@router.post("/{event_id}", response_model=EventRead)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    query = select(events).where(events.c.event_id == event_id)
    result = await session.execute(query)
    event_data = result.first()

    if not event_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    update_data = event_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    update_stmt = (
        update(events)
        .where(events.c.event_id == event_id)
        .values(**update_data)
        .returning(events)
    )

    result = await session.execute(update_stmt)
    await session.commit()

    updated_event = result.first()
    updated_event_dict = dict(zip(result.keys(), updated_event))
    updated_event_dict["id"] = updated_event_dict.pop("event_id")

    return EventRead(**updated_event_dict)
