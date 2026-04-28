from sqlalchemy import Column, ForeignKey, SmallInteger, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Section(Base):
    """
    Section model representing a classroom section within a grade.

    Attributes:
        id (str): Primary key, alphanumeric code (e.g., 'SR-001', 'SE-001').
        name (str): Full name of the section, must be unique.
        tag (str): Short tag/abbreviation for the section, unique.
        grade_id (int): Foreign key referencing the associated grade.
    """
    __tablename__ = "section"

    id = Column(String(6), primary_key=True, comment="Section code (e.g., 'SR-001', 'SE-001')")
    name = Column(String(25), nullable=False, unique=True, index=True, comment="Name of the section")
    tag = Column(String(10), unique=True, nullable=False, comment="Short tag/abbreviation for the section")
    grade_id = Column(
        SmallInteger,
        ForeignKey("grade.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="ID of the associated grade",
    )

    grade = relationship("Grade", back_populates="sections")
    enrollments = relationship("Enrollment", back_populates="section")
