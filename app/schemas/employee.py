from datetime import date, datetime

from pydantic import BaseModel, EmailStr, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    dni: str | None = None
    ruc: str | None = None
    gender: str | None = None
    birth_date: date | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    position: str | None = None
    address: str | None = None
