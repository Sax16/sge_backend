from sqlalchemy import SmallInteger, Boolean, Column, Date, DateTime, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import Gender, EmployeePosition
from app.models.base import Base


class Employee(Base):
    """
    Employee model representing company employees.
    
    Attributes:
        id: Primary key, auto-incremented, unique identifier for the employee
        first_name: Employee's first name
        last_name: Employee's last name
        dni: National ID document (DNI), unique identifier
        ruc: Tax identification number (optional)
        gender: Employee's gender (enum)
        birth_date: Date of birth
        phone_number: Contact phone number
        email: Contact email address
        is_active: Employment status flag
        position: Current position in company (enum)
        address: Physical address
        created_at: Record creation timestamp (auto-generated)
        updated_at: Last update timestamp (auto-updated)
    """
    __tablename__ = "employee"

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True, comment="Employee ID")
    first_name = Column(String(50), nullable=False, comment="Employee's first name")
    last_name = Column(String(50), nullable=False, comment="Employee's last name")
    dni = Column(String(15), nullable=False, unique=True, index=True, comment="National ID document (DNI)")
    ruc = Column(String(15), unique=True, comment="Tax identification number (optional)")
    gender = Column(Enum(Gender), nullable=False, comment="Employee's gender")
    birth_date = Column(Date, comment="Date of birth")
    phone_number = Column(String(15), nullable=False, comment="Contact phone number")
    email = Column(String(50), index=True, comment="Contact email address")
    address = Column(String(75), comment="Physical address")
    is_active = Column(Boolean, nullable=False, default=True, server_default="true", comment="Employment status flag")
    position = Column(Enum(EmployeePosition), nullable=False, comment="Current position in company")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    user = relationship("User", back_populates="employee", uselist=False)
    school_as_headmaster = relationship("School", foreign_keys="[School.headmaster_id]", back_populates="headmaster")
    school_as_deputy_director = relationship("School", foreign_keys="[School.deputy_director_id]", back_populates="deputy_director")
