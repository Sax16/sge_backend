from datetime import datetime

from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
