from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.models.base import Base


class ReceiptLine(Base):
    """
    ReceiptLine model representing each line/item inside a receipt mapped to a specific student charge.
    """
    __tablename__ = "receipt_line"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Receipt Line ID")
    charge_id = Column(Integer, ForeignKey("charge.id", ondelete="RESTRICT"), nullable=False, index=True, comment="Charge ID associated")
    receipt_id = Column(Integer, ForeignKey("receipt.id", ondelete="CASCADE"), index=True, comment="Receipt ID associated")
    amount = Column(Numeric(10, 2), nullable=False, comment="Amount applied to this line")

    charge = relationship("Charge", back_populates="receipt_lines")
    receipt = relationship("Receipt", back_populates="receipt_lines")
