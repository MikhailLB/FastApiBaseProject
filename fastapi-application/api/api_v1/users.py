from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from core.schemas.user import UserRead, UserCreate
from crud.users import get_all_users

router = APIRouter(
    tags=["users"],
)

@router.get("/users", response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await get_all_users(session=session)
    return users

@router.post("/add")
async def add_users(user: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    new_user = User(**user.model_dump())

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
