from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class Discount(Base):
    """
    Discount model representing the discounts available to apply to charges.
    """
    __tablename__ = "discount"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Discount ID")
    name = Column(String(50), nullable=False, comment="Discount name")
    amount = Column(Numeric(10, 2), nullable=False, comment="Discount amount")
    is_active = Column(Boolean, nullable=False, default=True, server_default="true", comment="Flag if discount is currently active")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    charge_discounts = relationship("ChargeDiscount", back_populates="discount")
