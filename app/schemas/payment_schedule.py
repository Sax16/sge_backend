from datetime import date as dateType, datetime

from pydantic import BaseModel, ConfigDict, Field


class PaymentScheduleBase(BaseModel):
    name: str = Field(..., description="Schedule name")
    start_date: dateType = Field(..., description="Start Date", alias="startDate")
    end_date: dateType = Field(..., description="End Date", alias="endDate")
    due_date: dateType = Field(..., description="Due Date", alias="dueDate")
    charge_catalog_id: int = Field(..., description="Charge Catalog ID", alias="chargeCatalogId")
    payment_scheme_id: int = Field(..., description="Payment Scheme ID", alias="paymentSchemeId")

    model_config = ConfigDict(populate_by_name=True)


class PaymentScheduleCreate(PaymentScheduleBase):
    pass


class PaymentScheduleRead(PaymentScheduleBase):
    id: int = Field(..., description="Payment Schedule ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaymentScheduleUpdate(PaymentScheduleBase):
    name: str | None = Field(None, description="Schedule name")
    start_date: dateType | None = Field(None, description="Start Date", alias="startDate")
    end_date: dateType | None = Field(None, description="End Date", alias="endDate")
    due_date: dateType | None = Field(None, description="Due Date", alias="dueDate")
    charge_catalog_id: int | None = Field(None, description="Charge Catalog ID", alias="chargeCatalogId")
    payment_scheme_id: int | None = Field(None, description="Payment Scheme ID", alias="paymentSchemeId")

    model_config = ConfigDict(populate_by_name=True)