from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from typing import List
from datetime import datetime

from src.auth.database import User, get_async_session
from src.Database.models import requests, events
from src.requests.schemas import RequestCreate, RequestRead, RequestUpdate
from src.auth.manager import current_user


router = APIRouter(
    prefix="/requests",
    tags=["Requests"]
)




@router.get("/me", response_model=List[RequestRead])
async def get_my_requests(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    query = (
        select(requests, events)
        .join(events, requests.c.event_id == events.c.event_id)
        .where(requests.c.user_id == current_user.id)
    )
    result = await session.execute(query)
    requests_data = result.fetchall()

    requests_dicts = [
        {
            "id": request.request_id,
            "user_id": request.user_id,
            "created_at": request.created_at,
            "updated_at": request.updated_at,
            "request_title": request.request_title,
            "event_title": event.title,
            "event_type": event.event_type
        }
        for request, event in requests_data
    ]

    return [RequestRead(**request_dict) for request_dict in requests_dicts]

@router.get("/{request_id}", response_model=RequestRead)
async def get_specific_request(request_id: int, session: AsyncSession = Depends(get_async_session)):
    query = (
        select(requests, events)
        .join(events, requests.c.event_id == events.c.event_id)
        .where(requests.c.request_id == request_id)
    )
    result = await session.execute(query)
    request_data = result.first()

    if not request_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

    request, event = request_data
    request_dict = {
        "id": request.request_id,
        "user_id": request.user_id,
        "created_at": request.created_at,
        "updated_at": request.updated_at,
        "request_title": request.request_title,
        "event_title": event.title,
        "event_type": event.event_type
    }

    return RequestRead(**request_dict)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_request(
    new_request: RequestCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    new_request_data = new_request.dict()
    new_request_data["user_id"] = current_user.id
    # new_request_data["created_at"] = text('NOW()')
    # new_request_data["updated_at"] = text('NOW()')
    statement = insert(requests).values(**new_request_data)
    await session.execute(statement)
    await session.commit()
    return {"status": "Request created"}

@router.post("/update", response_model=RequestRead)
async def update_request(
    request_update: RequestUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    query = select(requests).where(requests.c.request_id == request_update.id)
    result = await session.execute(query)
    request_data = result.first()

    if not request_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

    update_data = request_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    update_stmt = (
        update(requests)
        .where(requests.c.request_id == request_update.id)
        .values(**update_data)
        .returning(requests)
    )

    result = await session.execute(update_stmt)
    await session.commit()

    updated_request = result.first()
    updated_request_dict = dict(zip(result.keys(), updated_request))

    query_event = select(events).where(events.c.event_id == updated_request.event_id)
    result_event = await session.execute(query_event)
    event = result_event.first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    # updated_request_dict["event_title"] = event.title
    # updated_request_dict["event_type"] = event.event_type

    return RequestRead(**updated_request_dict)

