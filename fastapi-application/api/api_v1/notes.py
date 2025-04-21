from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from core.models import db_helper
from core.schemas.note import NoteResponse, NoteCreate, NoteUpdate
from crud.notes import get_all_notes, add_note, note_update, note_delete

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

@router.get("/get/{user_id}", response_model=list[NoteResponse], summary="Receive all notes")
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

@router.patch("/update/{note_id}", response_model=NoteResponse, summary="Update note")
async def update_note(note: NoteUpdate, note_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    """
        Update a note in database and return in case of success
    """
    try:
        updated_note = await note_update(session=session, note_data=note, id=note_id)
        if not updated_note:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update the note"
            )
        return updated_note

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating note: {str(e)}"
        )


@router.delete("/delete/{note_id}", response_model=NoteResponse, summary="Delete note")
async def delete_note(note_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    """
        Delete a note in database and return in case of success
        :param note_id:
        :param session:
        :return:
    """
    try:
        note = await note_delete(session=session, id=note_id)
        return note

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting note: {str(e)}")