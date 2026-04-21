from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PaymentSchemeBase(BaseModel):
    name: str = Field(..., description="Scheme name")

    model_config = ConfigDict(populate_by_name=True)


class PaymentSchemeCreate(PaymentSchemeBase):
    pass


class PaymentSchemeRead(PaymentSchemeBase):
    id: int = Field(..., description="Payment Scheme ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaymentSchemeUpdate(PaymentSchemeBase):
    name: str | None = Field(None, description="Scheme name")

    model_config = ConfigDict(populate_by_name=True)