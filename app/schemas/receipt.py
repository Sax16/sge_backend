from datetime import date as dateType, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import PaymentMethod, ReceiptType


class ReceiptBase(BaseModel):
    date: dateType = Field(..., description="Date of the receipt")
    total_amount: Decimal = Field(..., description="Total receipt amount", alias="totalAmount")
    guardian_id: int = Field(..., description="Guardian ID mapping the person paying", alias="guardianId")
    receipt_type: ReceiptType = Field(..., description="Type of receipt (Boleta, Factura, Otro)", alias="receiptType")
    user_id: int = Field(..., description="User ID who emitted the receipt", alias="userId")
    payment_method: PaymentMethod = Field(..., description="Method of payment", alias="paymentMethod")
    receipt_file_path: str | None = Field(None, description="Path to the digital receipt file", alias="receiptFilePath")
    payment_evidence_path: str | None = Field(None, description="Path to the evidence of payment file", alias="paymentEvidencePath")
    detail: str | None = Field(None, description="Optional detail/description")

    model_config = ConfigDict(populate_by_name=True)


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptRead(ReceiptBase):
    id: int = Field(..., description="Receipt ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ReceiptUpdate(ReceiptBase):
    date: dateType | None = Field(None, description="Date of the receipt")
    total_amount: Decimal | None = Field(None, description="Total receipt amount", alias="totalAmount")
    guardian_id: int | None = Field(None, description="Guardian ID mapping the person paying", alias="guardianId")
    receipt_type: ReceiptType | None = Field(None, description="Type of receipt (Boleta, Factura, Otro)", alias="receiptType")
    user_id: int | None = Field(None, description="User ID who emitted the receipt", alias="userId")
    payment_method: PaymentMethod | None = Field(None, description="Method of payment", alias="paymentMethod")
    receipt_file_path: str | None = Field(None, description="Path to the digital receipt file", alias="receiptFilePath")
    payment_evidence_path: str | None = Field(None, description="Path to the evidence of payment file", alias="paymentEvidencePath")
    detail: str | None = Field(None, description="Optional detail/description")

    model_config = ConfigDict(populate_by_name=True)