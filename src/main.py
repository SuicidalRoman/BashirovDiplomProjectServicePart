import subprocess
import ssl
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from src.auth.auth import auth_backend
from src.auth.database import User
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from src.profiles.profiles_router import router as profile_router
from src.requests.requests_router import router as request_router
from src.events.events_router import router as events_router

from src.config import SSL_KEY_FILE_PATH, SSL_CERT_FILE_PATH


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(
    certfile=SSL_CERT_FILE_PATH,
    keyfile=SSL_KEY_FILE_PATH
)


app = FastAPI(
    title="📱 Requests App Service",
    description="The service part of the diploma project by Ramil Bashirov",
    version="0.1.0"
)

app.add_middleware(HTTPSRedirectMiddleware)

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

app.include_router(
    router=events_router
)

app.include_router(router=profile_router)

app.include_router(router=request_router)

@app.get(path="/")
def main():
    return "Hello World!"


if __name__ == "__main__":
    subprocess.run(["uvicorn", "src/main:app", "--reload"])
