from datetime import date as dateType, datetime
from decimal import Decimal
from app.core.enums import ExpenseType

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    name: str = Field(..., description="Short description or name of the expense")
    amount: Decimal = Field(..., ge=0, le=9999.99, description="Expense amount")
    date: dateType = Field(..., description="Date when the expense occurred")
    expense_type: ExpenseType = Field(..., description="Type/Category of the expense", alias="expenseType")
    details: str | None = Field(None, description="Additional details or long description of the expense")

    model_config = ConfigDict(populate_by_name=True)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: int = Field(..., description="ID of the expense")
    user_id: int = Field(..., description="ID of the user who registered or is responsible for the expense", alias="userId")
    created_at: datetime = Field(..., description="Creation timestamp of the expense", alias="createdAt")
    updated_at: datetime = Field(..., description="Update timestamp of the expense", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ExpenseUpdate(ExpenseBase):
    name: str | None = Field(None, description="Short description or name of the expense")
    amount: Decimal | None = Field(None, ge=0, le=9999.99, description="Expense amount")
    date: dateType | None = Field(None, description="Date when the expense occurred")
    expense_type: ExpenseType | None = Field(None, description="Type/Category of the expense", alias="expenseType")
    details: str | None = Field(None, description="Additional details or long description of the expense")

    model_config = ConfigDict(populate_by_name=True)