from datetime import timedelta

from api.api_v1.auth.utils import encode_jwt
from core.config import settings
from core.schemas.user import UserRead

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_jwt(token_type: str, token_data: dict,
               expire_minutes: int = settings.auth_jwt.expire_minutes,
               expire_timedelta: timedelta | None = None) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    print(jwt_payload)
    return encode_jwt(payload=jwt_payload,
                      expire_minutes=expire_minutes,
                      expire_timedelta=expire_timedelta,)

def create_access_token(user: UserRead) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username
    }
    return create_jwt(token_type=ACCESS_TOKEN_TYPE, token_data=jwt_payload, expire_minutes=settings.auth_jwt.expire_minutes,)

def create_refresh_token(user: UserRead) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username
    }
    return create_jwt(token_type=REFRESH_TOKEN_TYPE, token_data=jwt_payload, expire_timedelta=timedelta(settings.auth_jwt.refresh_token_expire_days))