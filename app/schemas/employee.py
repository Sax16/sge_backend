from datetime import date, datetime
from app.core.enums import Gender, EmployeePosition

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class EmployeeBase(BaseModel):
    first_name: str = Field(..., description="First name of the employee", alias="firstName")
    last_name: str = Field(..., description="Last name of the employee", alias="lastName")
    dni: str = Field(..., description="DNI of the employee")
    ruc: str | None = Field(None, description="RUC of the employee")
    gender: Gender = Field(..., description="Gender of the employee")
    birth_date: date | None = Field(None, description="Birth date of the employee", alias="birthDate")
    address: str | None = Field(None, description="Address of the employee")
    phone_number: str | None = Field(None, description="Phone number of the employee", alias="phoneNumber")
    email: EmailStr | None = Field(None, description="Email of the employee")
    is_active: bool = Field(default=True, description="Active status of the employee", alias="isActive")
    position: EmployeePosition = Field(..., description="Position of the employee")

    model_config = ConfigDict(populate_by_name=True)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int = Field(..., description="ID of the employee")
    created_at: datetime = Field(..., description="Creation timestamp of the employee", alias="createdAt")
    updated_at: datetime = Field(..., description="Update timestamp of the employee", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class EmployeeUpdate(EmployeeBase):
    pass
