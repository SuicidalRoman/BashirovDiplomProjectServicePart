import subprocess
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead, UserUpdate

from profiles_router import router as profile_router
from requests.requests_router import router as request_router


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


app = FastAPI(
    title="📱 Requests App Service",
    description="The service part of the diploma project by Ramil Bashirov",
    version="0.1.0"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=False),
    prefix="/users",
    tags=["users"],
)

app.include_router(router=profile_router)

app.include_router(router=request_router)

@app.get(path="/")
def main():
    return "Hello World!"



if __name__ == "__main__":
    subprocess.run(["uvicorn", "main:app", "--reload"])
