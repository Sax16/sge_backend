from sqlalchemy import Column, DateTime, Enum, ForeignKey, SmallInteger, String, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base
from app.core.enums import ManagementType, Ugel


class School(Base):
    """
    School model representing the institution's general information.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier.
        company_name (str): Commercial name of the school (e.g., 'I.E. San José').
        business_name (str): Legal/registered business name of the institution.
        management (str): Name of the management or administrative unit.
        address (str): Physical address of the school.
        email (str): Institutional contact email.
        phone_number (str): Institutional contact phone number.
        logo_path (str): File path or URL to the school's logo (optional).
        ruc (str): Tax identification number (RUC).
        dre (str): Regional Education Directorate (DRE) name (optional).
        ugel (str): Local Education Management Unit (UGEL) name (optional).
        headmaster_id (int): Foreign key to the Employee acting as headmaster.
        deputy_director_id (int): Foreign key to the Employee acting as deputy director (optional).
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp of the last update.
    """
    __tablename__ = "school"

    __table_args__ = (
        CheckConstraint(
            'headmaster_id != deputy_director_id', 
            name='check_headmaster_neq_deputy'
        ),
    )

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True, comment="School ID")
    company_name = Column(String(255), nullable=False, comment="Commercial name of the school")
    business_name = Column(String(255), nullable=False, comment="Legal business name of the institution")
    management = Column(Enum(ManagementType), nullable=False, comment="Name of the management or administrative unit")
    address = Column(String(150), nullable=False, comment="Physical address of the school")
    email = Column(String(50), nullable=False, comment="Institutional contact email")
    phone_number = Column(String(15), nullable=False, comment="Institutional contact phone number")
    logo_path = Column(String(255), comment="File path or URL to the school's logo")
    ruc = Column(String(11), nullable=False, unique=True, comment="Tax identification number (RUC)")
    dre = Column(String(50), comment="Regional Education Directorate (DRE)")
    ugel = Column(Enum(Ugel), comment="Local Education Management Unit (UGEL)")
    headmaster_id = Column(
        SmallInteger,
        ForeignKey("employee.id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID of the headmaster (Employee)",
    )
    deputy_director_id = Column(
        SmallInteger,
        ForeignKey("employee.id", ondelete="RESTRICT"),
        comment="ID of the deputy director (Employee)",
    )
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    headmaster = relationship("Employee", foreign_keys=[headmaster_id], back_populates="school_as_headmaster")
    deputy_director = relationship("Employee", foreign_keys=[deputy_director_id], back_populates="school_as_deputy_director")
