from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    dni: str
    ruc: str | None = None
    gender: str
    birth_date: date | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    is_active: bool
    position: str
    address: str | None = None


class EmployeeCreate(EmployeeBase):
    create_at: datetime


class EmployeeRead(EmployeeBase):
    id: int
    create_at: datetime

    class Config:
        orm_mode = True
