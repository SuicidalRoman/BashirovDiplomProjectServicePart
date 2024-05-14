import pytest
from sqlalchemy import insert, select

from conftest import client, async_session_maker
from auth.database import User, UserStatus

async def test_register():
    response = client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "testPassword123",
        "user_status": UserStatus.CLIENT.value,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    })

    assert response.status_code == 201
