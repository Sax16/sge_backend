from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field, model_validator
from app.core.enums import ManagementType, Ugel


class SchoolBase(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=255, strip_whitespace=True, description="Commercial name of the school", alias="companyName")
    business_name: str = Field(..., min_length=2, max_length=255, strip_whitespace=True, description="Legal business name of the institution", alias="businessName")
    management: ManagementType = Field(..., description="Name of the management or administrative unit")
    address: str = Field(..., min_length=2, max_length=150, strip_whitespace=True, description="Physical address of the school")
    email: EmailStr = Field(..., max_length=50, description="Institutional contact email")
    phone_number: str = Field(..., pattern=r"^9\d{8}$", description="Institutional contact phone number", alias="phoneNumber")
    logo_path: str | None = Field(None, max_length=255, description="File path or URL to the school's logo", alias="logoPath")
    ruc: str = Field(..., pattern=r"^(10|20)\d{9}$", description="Tax identification number (RUC)")
    dre: str | None = Field(None, min_length=2, max_length=50, strip_whitespace=True, description="Regional Education Directorate (DRE)")
    ugel: Ugel | None = Field(None, description="Local Education Management Unit (UGEL)")
    headmaster_id: int = Field(..., gt=0, description="ID of the headmaster (Employee)", alias="headmasterId")
    deputy_director_id: int | None = Field(None, gt=0, description="ID of the deputy director (Employee)", alias="deputyDirectorId")

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode='after')
    def validate_different_directors(self):
        if self.deputy_director_id and self.headmaster_id == self.deputy_director_id:
            raise ValueError("El director y el subdirector no pueden ser la misma persona.")
        return self


class SchoolCreate(SchoolBase):
    pass


class SchoolRead(SchoolBase):
    id: int = Field(..., description="School ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SchoolUpdate(SchoolBase):
    pass
