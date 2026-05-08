from datetime import date as dateType, datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.core.enums import Gender, StudentStatus


class StudentBase(BaseModel):
    paternal_surname: str = Field(..., description="Student's paternal surname", alias="paternalSurname", min_length=2, max_length=75)
    maternal_surname: str = Field(..., description="Student's maternal surname", alias="maternalSurname", min_length=2, max_length=75)
    name: str = Field(..., description="Student's first and middle name(s)", min_length=2, max_length=150)
    dni: str = Field(..., description="National ID document (DNI)", pattern=r'^\d{8}$', min_length=8, max_length=8)
    gender: Gender = Field(..., description="Student's gender")
    birth_date: dateType | None = Field(None, description="Date of birth", alias="birthDate")
    address: str | None = Field(None, description="Physical address", min_length=2, max_length=150)
    phone_number: str | None = Field(None, description="Contact phone number", alias="phoneNumber", pattern=r"^9\d{8}$", min_length=9, max_length=9)
    email: EmailStr | None = Field(None, description="Contact email address")
    level: str | None = Field(None, description="Educational level name", min_length=2, max_length=25)
    grade: str | None = Field(None, description="Grade name", min_length=2, max_length=25)
    status: StudentStatus = Field(..., description="Enrollment status of the student")
    economic_level_id: int = Field(..., description="Economic level ID", alias="economicLevelId")

    model_config = ConfigDict(populate_by_name=True)


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int = Field(..., description="Student ID")
    economic_level_name: str | None = Field(None, description="Economic level name", alias="economicLevelName")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Record update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class StudentUpdate(StudentBase):
    paternal_surname: str | None = Field(None, description="Student's paternal surname", alias="paternalSurname", min_length=2, max_length=75)
    maternal_surname: str | None = Field(None, description="Student's maternal surname", alias="maternalSurname", min_length=2, max_length=75)
    name: str | None = Field(None, description="Student's first and middle name(s)", min_length=2, max_length=150)
    dni: str | None = Field(None, description="National ID document (DNI)", pattern=r'^\d{8}$', min_length=8, max_length=8)
    gender: Gender | None = Field(None, description="Student's gender")
    birth_date: dateType | None = Field(None, description="Date of birth", alias="birthDate")
    address: str | None = Field(None, description="Physical address", min_length=2, max_length=150)
    phone_number: str | None = Field(None, description="Contact phone number", alias="phoneNumber", pattern=r"^9\d{8}$", min_length=9, max_length=9)
    email: EmailStr | None = Field(None, description="Contact email address")
    level: str | None = Field(None, description="Educational level name", min_length=2, max_length=25)
    grade: str | None = Field(None, description="Grade name", min_length=2, max_length=25)
    status: StudentStatus | None = Field(None, description="Enrollment status of the student")
    economic_level_id: int | None = Field(None, description="Economic level ID", alias="economicLevelId")

    model_config = ConfigDict(populate_by_name=True)