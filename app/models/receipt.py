from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, SmallInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import PaymentMethod, ReceiptType
from app.models.base import Base


class Receipt(Base):
    """
    Receipt model representing a receipt or payment voucher issued for charges.
    """
    __tablename__ = "receipt"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Receipt ID")
    date = Column(Date, nullable=False, comment="Date of the receipt")
    total_amount = Column(Numeric(10, 2), nullable=False, comment="Total receipt amount")
    guardian_id = Column(Integer, ForeignKey("guardian.id", ondelete="RESTRICT"), nullable=False, index=True, comment="Guardian ID mapping the person paying")
    receipt_type = Column(Enum(ReceiptType), nullable=False, comment="Type of receipt (Boleta, Factura, Otro)")
    user_id = Column(SmallInteger, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False, index=True, comment="User ID who emitted the receipt")
    payment_method = Column(Enum(PaymentMethod), nullable=False, comment="Method of payment")
    receipt_file_path = Column(String(255), comment="Path to the digital receipt file")
    payment_evidence_path = Column(String(255), comment="Path to the evidence of payment file")
    detail = Column(String(100), comment="Optional detail/description")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")

    guardian = relationship("Guardian", back_populates="receipts")
    user = relationship("User", back_populates="receipts")
    receipt_lines = relationship("ReceiptLine", back_populates="receipt")
