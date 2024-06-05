import datetime
from typing import List
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

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
    profile_data = result.first()

    if not profile_data:
            return {"Error": "Profile not found"}
    
    profile_dict = dict(zip(result.keys(), profile_data))  # Преобразуем данные из tuple в словарь
    
    return profile_dict


@router.get("/all", response_model=List[ProfileRead])
async def get_all_profiles(session: AsyncSession = Depends(get_async_session)):
    """Admins may want to get all profiles"""
    query = select(profiles)

    try:
        result = await session.execute(query)
        profiles_data = result.all()
        profiles_dicts = []
        for profile_tuple in profiles_data:
            profile_dict = {
                "id": profile_tuple[0],
                "user_id": profile_tuple[1],
                "registered_at": profile_tuple[2],
                "updated_at": profile_tuple[3],
                "profile_type": profile_tuple[4].value,
                "surname": profile_tuple[5],
                "firstname": profile_tuple[6],
                "patronymic": profile_tuple[7],
                "birthdate": profile_tuple[8],
                "phone": profile_tuple[9]
            }
            profiles_dicts.append(profile_dict)
        return [ProfileRead(**profile_dict) for profile_dict in profiles_dicts]

    except Exception as e:
        return {"Error": f"{e}"}

@router.get("/{profile_id}")
async def get_specific_profile(profile_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(profiles).where(profiles.c.profile_id == profile_id)

    try:
        result = await session.execute(query)
        profile_data = result.first()

        if not profile_data:
            return {"Error": "Profile not found"}

        profile_dict = dict(zip(result.keys(), profile_data))

        return profile_dict
    except Exception as e:
        return None


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


@router.post("/me/update", response_model=ProfileRead)
async def update_my_profile(
    profile_update: ProfileUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    query = select(profiles).where(profiles.c.user_id == current_user.id)
    result = await session.execute(query)
    profile_data = result.first()

    if not profile_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    update_data = profile_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.datetime.utcnow()
    # update_data["registered_at"] = datetime.datetime.utcnow()

    update_stmt = (
        update(profiles)
        .where(profiles.c.user_id == current_user.id)
        .values(**update_data)
        .returning(profiles)
    )

    result = await session.execute(update_stmt)
    await session.commit()

    updated_profile = result.first()
    updated_profile_dict = dict(zip(result.keys(), updated_profile))
    updated_profile_dict["id"] = updated_profile_dict.pop("profile_id")

    return ProfileRead(**updated_profile_dict)