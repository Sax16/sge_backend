from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ReceiptLineBase(BaseModel):
    charge_id: int = Field(..., description="Charge ID associated", alias="chargeId")
    receipt_id: int | None = Field(None, description="Receipt ID associated", alias="receiptId")
    amount: Decimal = Field(..., description="Amount applied to this line")

    model_config = ConfigDict(populate_by_name=True)


class ReceiptLineCreate(ReceiptLineBase):
    pass


class ReceiptLineRead(ReceiptLineBase):
    id: int = Field(..., description="Receipt Line ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ReceiptLineUpdate(ReceiptLineBase):
    charge_id: int | None = Field(None, description="Charge ID associated", alias="chargeId")
    receipt_id: int | None = Field(None, description="Receipt ID associated", alias="receiptId")
    amount: Decimal | None = Field(None, description="Amount applied to this line")

    model_config = ConfigDict(populate_by_name=True)