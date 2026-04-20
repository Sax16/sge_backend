from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class PaymentSchedule(Base):
    """
    PaymentSchedule model representing schedule of payments based on scheme and charge.
    """
    __tablename__ = "payment_schedule"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Payment Schedule ID")
    name = Column(String(50), nullable=False, comment="Schedule name")
    start_date = Column(Date, nullable=False, comment="Start Date")
    end_date = Column(Date, nullable=False, comment="End Date")
    due_date = Column(Date, nullable=False, comment="Due Date")
    charge_catalog_id = Column(Integer, ForeignKey("charge_catalog.id", ondelete="CASCADE"), nullable=False, index=True, comment="Charge Catalog ID")
    payment_scheme_id = Column(Integer, ForeignKey("payment_scheme.id", ondelete="CASCADE"), nullable=False, index=True, comment="Payment Scheme ID")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    charge_catalog = relationship("ChargeCatalog", back_populates="payment_schedules")
    payment_scheme = relationship("PaymentScheme", back_populates="payment_schedules")
