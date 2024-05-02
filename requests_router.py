from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session


router = APIRouter(
    prefix="/requests",
    tags=["Requests"]
)


@router.get("/")
async def get_all_requests(session: AsyncSession = Depends(get_async_session)):
    pass