from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.auth.helpers import TOKEN_TYPE_FIELD, REFRESH_TOKEN_TYPE, ACCESS_TOKEN_TYPE
from api.api_v1.auth.utils import decode_jwt
from core.models import db_helper, User
from core.schemas.user import UserCreate, UserRead
from crud.users import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://localhost:8000/api/jwt/login/')
refresh_token_scheme = OAuth2PasswordBearer(tokenUrl='http://localhost:8000/api/jwt/refresh/')
def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> UserCreate:
   try:
       payload = decode_jwt(token=token)
   except InvalidTokenError as e:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

   return payload

def validate_token_type(payload: dict,
                        token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    print(payload)
    print(current_token_type)
    print(token_type)
    if current_token_type == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Invalid token type {token_type} expected {REFRESH_TOKEN_TYPE}")

async def get_user_by_token_sub(payload: dict, session: AsyncSession) -> User:
    username: str | None = payload.get("username")
    user = await get_user(session, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="token invalid (user not found)")
    return user

def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(payload: dict = Depends(get_current_token_payload), session: AsyncSession = Depends(db_helper.session_getter)) -> User:
       validate_token_type(payload, token_type=token_type)
       return await get_user_by_token_sub(payload, session)
    return get_auth_user_from_token

get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)



