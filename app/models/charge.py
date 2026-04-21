from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import ChargeStatus
from app.models.base import Base


class Charge(Base):
    """
    Charge model representing a specific charge assigned to a student.
    """
    __tablename__ = "charge"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Charge ID")
    charge_catalog_id = Column(Integer, ForeignKey("charge_catalog.id", ondelete="RESTRICT"), nullable=False, index=True, comment="Charge Catalog ID")
    status = Column(Enum(ChargeStatus), nullable=False, default=ChargeStatus.PENDIENTE, comment="Status of the charge")
    amount = Column(Numeric(10, 2), nullable=False, comment="Total initial amount")
    payment_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="Amount already paid")
    discount_amount = Column(Numeric(10, 2), default=0, comment="Total discounted amount")
    due_date = Column(Date, nullable=False, comment="Due date")
    student_id = Column(Integer, ForeignKey("student.id", ondelete="RESTRICT"), nullable=False, index=True, comment="Student ID")
    user_id = Column(SmallInteger, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False, index=True, comment="User ID")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    charge_catalog = relationship("ChargeCatalog", back_populates="charges")
    student = relationship("Student", back_populates="charges")
    charge_discounts = relationship("ChargeDiscount", back_populates="charge")
    user = relationship("User", back_populates="charges")
    receipt_lines = relationship("ReceiptLine", back_populates="charge")
