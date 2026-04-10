from sqlalchemy import Column, Date, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from app.core.enums import EconomicLevel, StudentStatus, Gender
from app.models.base import Base


class Student(Base):
    """
    Student model representing enrolled students in the institution.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier.
        paternal_surname (str): Student's paternal surname.
        maternal_surname (str): Student's maternal surname.
        name (str): Student's first and middle name(s).
        dni (str): National ID document, unique identifier.
        gender (Gender): Student's gender (enum).
        birth_date (date): Date of birth.
        address (str): Physical address (optional).
        phone_number (str): Contact phone number (optional).
        email (str): Contact email address (optional).
        level (str): Educational level name (e.g., 'Primaria').
        grade (str): Grade name (e.g., '1er Grado').
        status (StudentStatus): Enrollment status of the student (enum).
        economic_level (EconomicLevel): Socioeconomic level classification (enum).
        created_at (datetime): Timestamp when the record was created.
    """
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Student ID")
    paternal_surname = Column(String(75), nullable=False, comment="Student's paternal surname")
    maternal_surname = Column(String(75), nullable=False, comment="Student's maternal surname")
    name = Column(String(150), nullable=False, comment="Student's first and middle name(s)")
    dni = Column(String(12), nullable=False, unique=True, index=True, comment="National ID document (DNI)")
    gender = Column(Enum(Gender), comment="Student's gender")
    birth_date = Column(Date, comment="Date of birth")
    address = Column(String(150), comment="Physical address")
    phone_number = Column(String(15), comment="Contact phone number")
    email = Column(String(50), index=True, comment="Contact email address")
    level = Column(String(25), nullable=False, comment="Educational level name")
    grade = Column(String(25), nullable=False, comment="Grade name")
    status = Column(Enum(StudentStatus), nullable=False, comment="Enrollment status of the student")
    economic_level = Column(Enum(EconomicLevel), nullable=False, comment="Socioeconomic level classification")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Record update timestamp")
