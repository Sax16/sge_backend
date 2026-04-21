from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class ChargeDiscount(Base):
    """
    ChargeDiscount associative model representing the discount(s) applied to a specific charge.
    """
    __tablename__ = "charge_discount"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Charge Discount ID")
    charge_id = Column(Integer, ForeignKey("charge.id", ondelete="CASCADE"), nullable=False, index=True, comment="Charge ID")
    discount_id = Column(Integer, ForeignKey("discount.id", ondelete="CASCADE"), nullable=False, index=True, comment="Discount ID")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    charge = relationship("Charge", back_populates="charge_discounts")
    discount = relationship("Discount", back_populates="charge_discounts")
