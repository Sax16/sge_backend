from datetime import date as dateType, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import AcademicPeriodType


class AcademicPeriodBase(BaseModel):
    name: str = Field(..., description="Name of the academic period")
    start_date: dateType = Field(..., description="Start date of the academic period", alias="startDate")
    end_date: dateType = Field(..., description="End date of the academic period", alias="endDate")
    is_active: bool = Field(default=False, description="Active status of the academic period", alias="isActive")
    year: int = Field(..., description="Year of the academic period")
    type: AcademicPeriodType = Field(..., description="Type of the academic period")

    model_config = ConfigDict(populate_by_name=True)


class AcademicPeriodCreate(AcademicPeriodBase):
    pass


class AcademicPeriodRead(AcademicPeriodBase):
    id: int = Field(..., description="Academic period ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class AcademicPeriodUpdate(AcademicPeriodBase):
    name: str | None = Field(None, description="Name of the academic period")
    start_date: dateType | None = Field(None, description="Start date of the academic period", alias="startDate")
    end_date: dateType | None = Field(None, description="End date of the academic period", alias="endDate")
    is_active: bool | None = Field(None, description="Active status of the academic period", alias="isActive")
    year: int | None = Field(None, description="Year of the academic period")
    type: AcademicPeriodType | None = Field(None, description="Type of the academic period")

    model_config = ConfigDict(populate_by_name=True)