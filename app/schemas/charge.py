from datetime import date as dateType, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import ChargeStatus


class ChargeBase(BaseModel):
    charge_catalog_id: int = Field(..., description="Charge Catalog ID", alias="chargeCatalogId")
    status: ChargeStatus = Field(default=ChargeStatus.PENDIENTE, description="Status of the charge")
    amount: Decimal = Field(..., description="Total initial amount")
    payment_amount: Decimal = Field(default=0, description="Amount already paid", alias="paymentAmount")
    discount_amount: Decimal = Field(default=0, description="Total discounted amount", alias="discountAmount")
    due_date: dateType = Field(..., description="Due date", alias="dueDate")
    student_id: int = Field(..., description="Student ID", alias="studentId")
    user_id: int = Field(..., description="User ID", alias="userId")

    model_config = ConfigDict(populate_by_name=True)


class ChargeCreate(ChargeBase):
    pass


class ChargeRead(ChargeBase):
    id: int = Field(..., description="Charge ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ChargeUpdate(ChargeBase):
    charge_catalog_id: int | None = Field(None, description="Charge Catalog ID", alias="chargeCatalogId")
    status: ChargeStatus | None = Field(None, description="Status of the charge")
    amount: Decimal | None = Field(None, description="Total initial amount")
    payment_amount: Decimal | None = Field(None, description="Amount already paid", alias="paymentAmount")
    discount_amount: Decimal | None = Field(None, description="Total discounted amount", alias="discountAmount")
    due_date: dateType | None = Field(None, description="Due date", alias="dueDate")
    student_id: int | None = Field(None, description="Student ID", alias="studentId")
    user_id: int | None = Field(None, description="User ID", alias="userId")

    model_config = ConfigDict(populate_by_name=True)