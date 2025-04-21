from typing import Sequence, List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Note
from core.schemas.note import NoteCreate, NoteResponse, NoteUpdate


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

async def note_update(session: AsyncSession, id: int, note_data: NoteUpdate) -> Note:
    try:
        query = select(Note).filter(Note.id == id)
        result = await session.execute(query)
        note = result.scalar_one()
        data_dict = note_data.model_dump(exclude_unset=True)

        for key, value in data_dict.items():
            setattr(note, key, value)

        await session.commit()
        await session.refresh(note)

        return note

    except SQLAlchemyError as e:
        raise NoResultFound(f"Note with id {id} not found.")


async def note_delete(session: AsyncSession, id: int) -> Note:
    try:
        query = select(Note).filter(Note.id == id)
        result = await session.execute(query)
        note = result.scalar_one_or_none()

        if note is None:
            raise NoResultFound(f"Note with id {id} not found.")

        await session.delete(note)
        await session.commit()

    except SQLAlchemyError as e:
        raise SQLAlchemyError(e)

    return note