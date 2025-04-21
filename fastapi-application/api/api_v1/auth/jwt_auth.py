from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi.security import HTTPBearer
from api.api_v1.auth import utils as auth_utils
from api.api_v1.auth.helpers import create_access_token, create_refresh_token
from api.api_v1.auth.validation import get_current_auth_user_for_refresh, get_current_auth_user
from core.models import db_helper
from core.schemas.user import UserRead
from crud.users import get_user


http_bearer = HTTPBearer()
router = APIRouter(prefix="/jwt", tags=["JWT"])

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str = "Bearer"


async def validate_auth_user(username: str = Form(), password: str = Form(), session: AsyncSession = Depends(db_helper.session_getter)):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    user = await get_user(session, username)
    if not user:
        raise unauthed_exc
    if auth_utils.validate_password(password, hashed_password=user.password):
        return user

    raise unauthed_exc

@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
        user: UserRead = Depends(validate_auth_user),
):
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/", response_model=TokenInfo, response_model_exclude_none=True)
async def auth_refresh_jwt(user: UserRead = Depends(get_current_auth_user_for_refresh), ):
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.get("/users/me/")
def auth_user_check_self_info(
        user: UserRead = Depends(get_current_auth_user),
):
    return {
        "username": user.username,
        "id": user.id,

    }