from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from core.models import db_helper
from core.schemas.note import NoteResponse, NoteCreate
from crud.notes import get_all_notes, add_note

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

@router.get("/get", response_model=list[NoteResponse], summary="Receive all notes")
async def get_notes(user_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    """
        Return a list of all notes
    """
    try:
        notes = await get_all_notes(session=session, user_id=user_id)
        if not notes:
            return []
        return notes
    except Exception as e:
        raise HTTPException(
                            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error while retrieving notes {str(e)}"
                            )

@router.post("/add", response_model=NoteResponse, summary="Add new note")
async def add_note_ep(note: NoteCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    """
        Add a new note in database and return in case of success
    """
    try:
        created_note = await add_note(session=session, note=note)
        if not created_note:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create the note"
            )
        return created_note
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating note: {str(e)}"
        )