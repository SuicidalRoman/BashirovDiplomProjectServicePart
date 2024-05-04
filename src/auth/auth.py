from fastapi_users.authentication import  CookieTransport, JWTStrategy, AuthenticationBackend
from src.config import SECRET_PHRASE


cookie_transport = CookieTransport(
    cookie_name="business_dialog_cookie",
    cookie_max_age=3600
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_PHRASE, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
