from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Integer, SmallInteger, String
from sqlalchemy.sql import func

from app.core.enums import AcademicPeriodType
from app.models.base import Base


class AcademicPeriod(Base):
    """
    AcademicPeriod model representing a specific academic period within the school year
    (e.g., '2025-1').

    Attributes:
        id (int): Primary key, auto-incremented unique identifier.
        name (str): Full name of the academic period, must be unique.
        start_date (date): Start date of the academic period.
        end_date (date): End date of the academic period.
        is_active (bool): Indicates whether this is the currently active period.
        year (int): Year of the academic period.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp of the last update (auto-updated).
        type (AcademicPeriodType): Type of the academic period (enum).
    """
    __tablename__ = "academic_period"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Academic period ID")
    name = Column(String(25), nullable=False, unique=True, index=True, comment="Name of the academic period")
    start_date = Column(Date, nullable=False, comment="Start date of the academic period")
    end_date = Column(Date, nullable=False, comment="End date of the academic period")
    is_active = Column(Boolean, nullable=False, default=False, server_default="false", comment="Active status of the academic period")
    year = Column(SmallInteger, nullable=False, comment="Year of the academic period")
    type = Column(Enum(AcademicPeriodType), nullable=False, comment="Type of the academic period")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")
