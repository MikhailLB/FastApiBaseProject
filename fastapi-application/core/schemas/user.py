from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: bytes

class UserRead(UserBase):
    id: int

