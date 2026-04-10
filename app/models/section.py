from sqlalchemy import Column, DateTime, Enum, ForeignKey, SmallInteger, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.enums import SectionType
from app.models.base import Base


class Section(Base):
    """
    Section model representing a classroom section within a grade.

    Attributes:
        id (str): Primary key, alphanumeric code (e.g., '1A', '2B').
        name (str): Full name of the section, must be unique.
        tag (str): Short tag/abbreviation for the section, unique.
        type (SectionType): Type/modality of the section.
        grade_id (int): Foreign key referencing the associated grade.
        updated_at (datetime): Timestamp of the last update (auto-updated).
    """
    __tablename__ = "section"

    id = Column(String(6), primary_key=True, comment="Section code (e.g., '1A', '2B')")
    name = Column(String(25), nullable=False, unique=True, index=True, comment="Name of the section")
    tag = Column(String(10), unique=True, nullable=False, comment="Short tag/abbreviation for the section")
    type = Column(Enum(SectionType), nullable=False, comment="Type or modality of the section")
    grade_id = Column(
        SmallInteger,
        ForeignKey("grade.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="ID of the associated grade",
    )
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    grade = relationship("Grade", back_populates="sections")
