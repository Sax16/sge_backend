from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class PaymentScheme(Base):
    """
    PaymentScheme model representing different payment plans or schemes.
    """
    __tablename__ = "payment_scheme"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Payment Scheme ID")
    name = Column(String(50), nullable=False, comment="Scheme name")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    payment_schedules = relationship("PaymentSchedule", back_populates="payment_scheme")
    enrollments = relationship("Enrollment", back_populates="payment_scheme")
