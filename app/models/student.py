from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import StudentStatus, Gender
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
    dni = Column(String(8), nullable=False, unique=True, index=True, comment="National ID document (DNI)")
    gender = Column(Enum(Gender), nullable=False, comment="Student's gender")
    birth_date = Column(Date, nullable=False, comment="Date of birth")
    address = Column(String(150), comment="Physical address")
    phone_number = Column(String(9), comment="Contact phone number")
    email = Column(String(50), index=True, comment="Contact email address")
    level = Column(String(25), comment="Educational level name")
    grade = Column(String(25), comment="Grade name")
    status = Column(Enum(StudentStatus), nullable=False, comment="Enrollment status of the student")
    economic_level_id = Column(Integer, ForeignKey("economic_level.id"), nullable=False, index=True, comment="Economic level ID")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Record update timestamp")

    guardians = relationship("GuardianStudent", back_populates="student")
    economic_level = relationship("EconomicLevel", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    charges = relationship("Charge", back_populates="student")

    @property
    def economic_level_name(self) -> str | None:
        """Returns the name of the associated economic level."""
        return self.economic_level.name if self.economic_level else None
