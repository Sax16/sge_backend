from datetime import date as dateType, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import EnrollmentStatus


class EnrollmentBase(BaseModel):
    payment_scheme_id: int = Field(..., description="Payment Scheme ID", alias="paymentSchemeId")
    academic_period_id: int = Field(..., description="Academic Period ID", alias="academicPeriodId")
    date: dateType = Field(..., description="Date of enrollment")
    section_id: str = Field(..., description="Section ID", alias="sectionId")
    student_id: int = Field(..., description="Student ID", alias="studentId")
    user_id: int = Field(..., description="User ID who registered enrollment", alias="userId")
    status: EnrollmentStatus = Field(default=EnrollmentStatus.ACTIVO, description="Status of the enrollment")

    model_config = ConfigDict(populate_by_name=True)


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    id: int = Field(..., description="Enrollment ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class EnrollmentUpdate(EnrollmentBase):
    payment_scheme_id: int | None = Field(None, description="Payment Scheme ID", alias="paymentSchemeId")
    academic_period_id: int | None = Field(None, description="Academic Period ID", alias="academicPeriodId")
    date: dateType | None = Field(None, description="Date of enrollment")
    section_id: str | None = Field(None, description="Section ID", alias="sectionId")
    student_id: int | None = Field(None, description="Student ID", alias="studentId")
    user_id: int | None = Field(None, description="User ID who registered enrollment", alias="userId")
    status: EnrollmentStatus | None = Field(None, description="Status of the enrollment")

    model_config = ConfigDict(populate_by_name=True)