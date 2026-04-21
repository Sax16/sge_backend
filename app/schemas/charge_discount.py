from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChargeDiscountBase(BaseModel):
    charge_id: int = Field(..., description="Charge ID", alias="chargeId")
    discount_id: int = Field(..., description="Discount ID", alias="discountId")

    model_config = ConfigDict(populate_by_name=True)


class ChargeDiscountCreate(ChargeDiscountBase):
    pass


class ChargeDiscountRead(ChargeDiscountBase):
    id: int = Field(..., description="Charge Discount ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ChargeDiscountUpdate(ChargeDiscountBase):
    charge_id: int | None = Field(None, description="Charge ID", alias="chargeId")
    discount_id: int | None = Field(None, description="Discount ID", alias="discountId")

    model_config = ConfigDict(populate_by_name=True)