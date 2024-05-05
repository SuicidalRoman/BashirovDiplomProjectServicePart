from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.auth.database import get_async_session, User
from src.Database.models import profiles
from src.profiles.schemas import (ProfileCreate, ProfileRead, ProfileUpdate)
from src.auth.manager import current_user


router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)

@router.get("/me")
async def get_my_profile(session: AsyncSession = Depends(get_async_session),
                         current_user: User = Depends(current_user)):
    query = select(profiles).where(profiles.c.user_id == current_user.id)
    result = await session.execute(query)
    return {
            "status": "success",
            "data": result.all(),
            "details": None
        }

@router.post("/me/create")
async def create_new_profile(
    new_profile: ProfileCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    new_profile.user_id = current_user.id
    statement = insert(profiles).values(**new_profile.dict())
    await session.execute(statement=statement)
    await session.commit()
    return {"status": "200"}