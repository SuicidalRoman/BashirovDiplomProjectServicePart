from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.auth.database import User, get_async_session
from src.Database.models import requests
from src.requests.schemas import RequestCreate
from src.auth.manager import current_user


router = APIRouter(
    prefix="/requests",
    tags=["Requests"]
)



@router.get("/")
async def get_all_requests(session: AsyncSession = Depends(get_async_session)):
    """Fetch all requests"""
    query = select(requests)
    result = await session.execute(query)
    return result.all()

@router.get("/me")
async def get_my_requests(
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
    ):
    query = select(requests).where(requests.c.user_id == current_user.id)
    result = await session.execute(query)
    return result.all()

@router.post("/me")
async def create_request(
    new_request: RequestCreate,
    current_user: User = Depends(current_user), 
    session: AsyncSession = Depends(get_async_session)
    ):
    """Create a new request"""
    new_request.user_id = current_user.id
    statement = insert(requests).values(**new_request.dict())
    result = await session.execute(statement)
    return result

