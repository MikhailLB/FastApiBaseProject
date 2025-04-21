from Tools.scripts.summarize_stats import print_specialization_stats
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi_jwt import JwtAccessBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.utils import hash_password
from core.models import db_helper, User
from core.schemas.user import UserRead, UserCreate, UserBase
from crud.users import get_all_users, get_user

router = APIRouter(
    tags=["users"],
)

@router.get("/users", response_model=list[UserCreate])
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await get_all_users(session=session)
    return users

@router.post("/add")
async def add_users(username: str = Form(), password: str = Form(), session: AsyncSession = Depends(db_helper.session_getter)):

    password = hash_password(password)
    new_user = User(username=username, password=password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


