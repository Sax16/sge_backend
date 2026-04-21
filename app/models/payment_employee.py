from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class PaymentEmployee(Base):
    """
    PaymentEmployee model representing payments (e.g., salaries, stipends) made to an employee.
    """
    __tablename__ = "payment_employee"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Payment ID")
    name = Column(String(100), nullable=False, comment="Name or title of the payment")
    amount = Column(Numeric(10, 2), nullable=False, comment="Amount paid")
    date = Column(Date, nullable=False, comment="Date of the payment")
    detail = Column(String(100), comment="Optional detail about payment")
    user_id = Column(SmallInteger, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False, index=True, comment="User ID who recorded the payment")
    employee_id = Column(SmallInteger, ForeignKey("employee.id", ondelete="RESTRICT"), nullable=False, index=True, comment="Employee ID receiving the payment")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    user = relationship("User", back_populates="employee_payments")
    employee = relationship("Employee", back_populates="payments_received")
