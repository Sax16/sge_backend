from datetime import date as dateType, datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class GuardianBase(BaseModel):
    first_name: str = Field(..., description="Guardian's first name", alias="firstName")
    last_name: str = Field(..., description="Guardian's last name", alias="lastName")
    dni: str = Field(..., description="National ID document (DNI)")
    ruc: str | None = Field(None, description="Tax identification number (optional)")
    birth_date: dateType | None = Field(None, description="Date of birth", alias="birthDate")
    phone_number: str | None = Field(None, description="Contact phone number", alias="phoneNumber")
    email: EmailStr | None = Field(None, description="Contact email address")
    address: str | None = Field(None, description="Physical address")

    model_config = ConfigDict(populate_by_name=True)


class GuardianCreate(GuardianBase):
    pass


class GuardianRead(GuardianBase):
    id: int = Field(..., description="Guardian ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class GuardianUpdate(GuardianBase):
    first_name: str | None = Field(None, description="Guardian's first name", alias="firstName")
    last_name: str | None = Field(None, description="Guardian's last name", alias="lastName")
    dni: str | None = Field(None, description="National ID document (DNI)")
    ruc: str | None = Field(None, description="Tax identification number (optional)")
    birth_date: dateType | None = Field(None, description="Date of birth", alias="birthDate")
    phone_number: str | None = Field(None, description="Contact phone number", alias="phoneNumber")
    email: EmailStr | None = Field(None, description="Contact email address")
    address: str | None = Field(None, description="Physical address")

    model_config = ConfigDict(populate_by_name=True)