from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str
    is_active: bool
    employee_id: int


class UserCreate(UserBase):
    password: str
    create_at: datetime


class UserRead(UserBase):
    id: int
    create_at: datetime

    class Config:
        orm_mode = True
