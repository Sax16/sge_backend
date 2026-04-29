from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class SchoolBase(BaseModel):
    company_name: str = Field(..., max_length=255, description="Commercial name of the school", alias="companyName")
    business_name: str = Field(..., max_length=255, description="Legal business name of the institution", alias="businessName")
    management: str = Field(..., max_length=50, description="Name of the management or administrative unit")
    address: str = Field(..., max_length=150, description="Physical address of the school")
    email: EmailStr = Field(..., max_length=50, description="Institutional contact email")
    phone_number: str = Field(..., max_length=15, description="Institutional contact phone number", alias="phoneNumber")
    logo_path: str | None = Field(None, max_length=255, description="File path or URL to the school's logo", alias="logoPath")
    ruc: str = Field(..., max_length=15, description="Tax identification number (RUC)")
    dre: str | None = Field(None, max_length=50, description="Regional Education Directorate (DRE)")
    ugel: str | None = Field(None, max_length=50, description="Local Education Management Unit (UGEL)")
    headmaster_id: int = Field(..., description="ID of the headmaster (Employee)", alias="headmasterId")
    deputy_director_id: int | None = Field(None, description="ID of the deputy director (Employee)", alias="deputyDirectorId")

    model_config = ConfigDict(populate_by_name=True)


class SchoolCreate(SchoolBase):
    pass


class SchoolRead(SchoolBase):
    id: int = Field(..., description="School ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SchoolUpdate(SchoolBase):
    company_name: str | None = Field(None, max_length=255, description="Commercial name of the school", alias="companyName")
    business_name: str | None = Field(None, max_length=255, description="Legal business name of the institution", alias="businessName")
    management: str | None = Field(None, max_length=50, description="Name of the management or administrative unit")
    address: str | None = Field(None, max_length=150, description="Physical address of the school")
    email: EmailStr | None = Field(None, max_length=50, description="Institutional contact email")
    phone_number: str | None = Field(None, max_length=15, description="Institutional contact phone number", alias="phoneNumber")
    logo_path: str | None = Field(None, max_length=255, description="File path or URL to the school's logo", alias="logoPath")
    ruc: str | None = Field(None, max_length=15, description="Tax identification number (RUC)")
    dre: str | None = Field(None, max_length=50, description="Regional Education Directorate (DRE)")
    ugel: str | None = Field(None, max_length=50, description="Local Education Management Unit (UGEL)")
    headmaster_id: int | None = Field(None, description="ID of the headmaster (Employee)", alias="headmasterId")
    deputy_director_id: int | None = Field(None, description="ID of the deputy director (Employee)", alias="deputyDirectorId")
