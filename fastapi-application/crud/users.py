from typing import Sequence, List

from fastapi.params import Depends
from fastapi_jwt import JwtAccessBearer
from fastapi_jwt.jwt import JwtAccess
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_helper
from core.schemas.user import UserBase


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()

async def get_user(session: AsyncSession, username: str) -> User:
    query = select(User).filter(User.username == username)
    result = await session.execute(query)
    user = result.scalar_one()
    return user