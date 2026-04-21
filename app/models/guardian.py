from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class Guardian(Base):
    """
    Guardian model representing a student's parent, tutor, or guardian.
    
    Attributes:
        id: Primary key, auto-incremented, unique identifier
        first_name: Guardian's first name
        last_name: Guardian's last name
        dni: National ID document (DNI)
        ruc: Tax identification number (optional)
        birth_date: Date of birth (optional)
        phone_number: Contact phone number (optional)
        email: Contact email address (optional)
        address: Physical address (optional)
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "guardian"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Guardian ID")
    first_name = Column(String(50), nullable=False, comment="Guardian's first name")
    last_name = Column(String(50), nullable=False, comment="Guardian's last name")
    dni = Column(String(15), nullable=False, unique=True, index=True, comment="National ID document (DNI)")
    ruc = Column(String(15), unique=True, comment="Tax identification number (optional)")
    birth_date = Column(Date, comment="Date of birth")
    phone_number = Column(String(15), comment="Contact phone number")
    email = Column(String(50), index=True, comment="Contact email address")
    address = Column(String(75), comment="Physical address")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    students = relationship("GuardianStudent", back_populates="guardian")
    receipts = relationship("Receipt", back_populates="guardian")
