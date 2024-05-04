from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.database import get_async_session


router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)