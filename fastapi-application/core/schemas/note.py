from datetime import datetime

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    name: str = Field(..., title="Название", min_length=1, max_length=255)
    description: str | None = Field(None, title="Описание", max_length=1000)
    is_completed: bool = Field(False, title="Статус завершения")

class NoteCreate(NoteBase):
    user_id: int = Field(..., title="ID пользователя")

class NoteUpdate(BaseModel):
    name: str | None = Field(None, title="Название", min_length=1, max_length=255)
    description: str | None = Field(None, title="Описание", max_length=1000)
    is_completed: bool | None = Field(None, title="Статус завершения")

class NoteResponse(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

