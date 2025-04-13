from enum import unique
from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from .base import Base

class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    notes: Mapped[List["Note"]] = relationship("Note", back_populates="user")