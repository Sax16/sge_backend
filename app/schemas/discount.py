from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class DiscountBase(BaseModel):
    name: str = Field(..., description="Discount name")
    amount: Decimal = Field(..., description="Discount amount")
    is_active: bool = Field(default=True, description="Flag if discount is currently active", alias="isActive")

    model_config = ConfigDict(populate_by_name=True)


class DiscountCreate(DiscountBase):
    pass


class DiscountRead(DiscountBase):
    id: int = Field(..., description="Discount ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class DiscountUpdate(DiscountBase):
    name: str | None = Field(None, description="Discount name")
    amount: Decimal | None = Field(None, description="Discount amount")
    is_active: bool | None = Field(None, description="Flag if discount is currently active", alias="isActive")

    model_config = ConfigDict(populate_by_name=True)