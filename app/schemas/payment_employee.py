from datetime import date as dateType, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentEmployeeBase(BaseModel):
    name: str = Field(..., description="Name or title of the payment")
    amount: Decimal = Field(..., description="Amount paid")
    date: dateType = Field(..., description="Date of the payment")
    detail: str | None = Field(None, description="Optional detail about payment")
    user_id: int = Field(..., description="User ID who recorded the payment", alias="userId")
    employee_id: int = Field(..., description="Employee ID receiving the payment", alias="employeeId")

    model_config = ConfigDict(populate_by_name=True)


class PaymentEmployeeCreate(PaymentEmployeeBase):
    pass


class PaymentEmployeeRead(PaymentEmployeeBase):
    id: int = Field(..., description="Payment ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaymentEmployeeUpdate(PaymentEmployeeBase):
    name: str | None = Field(None, description="Name or title of the payment")
    amount: Decimal | None = Field(None, description="Amount paid")
    date: dateType | None = Field(None, description="Date of the payment")
    detail: str | None = Field(None, description="Optional detail about payment")
    user_id: int | None = Field(None, description="User ID who recorded the payment", alias="userId")
    employee_id: int | None = Field(None, description="Employee ID receiving the payment", alias="employeeId")

    model_config = ConfigDict(populate_by_name=True)