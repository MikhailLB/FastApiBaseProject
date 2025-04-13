from typing import Sequence, List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Note
from core.schemas.note import NoteCreate, NoteResponse


async def get_all_notes(session: AsyncSession, user_id: int) -> Sequence[Note]:
    try:
        stmt = await session.execute(select(Note).filter(Note.user_id == user_id))
        result = stmt.scalars().all()
        return result
    except SQLAlchemyError as e:
        raise e


async def add_note(session: AsyncSession, note: NoteCreate) -> Note:
    try:
        new_note = Note(**note.model_dump())

        session.add(new_note)
        await session.commit()
        await session.refresh(new_note)

        return new_note

    except SQLAlchemyError as e:
        await session.rollback()
        raise e