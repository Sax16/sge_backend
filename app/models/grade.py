from sqlalchemy import Column, ForeignKey, SmallInteger, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Grade(Base):
    """
    Grade model representing academic grades (e.g., 1st grade, 2nd grade).

    Attributes:
        id (int): Primary key, auto-incremented unique identifier.
        name (str): Full name of the grade, must be unique.
        tag (str): Short tag/abbreviation for the grade, unique.
        level_id (int): Foreign key referencing the associated educational level.
        sections: List of sections belonging to this grade.
    """
    __tablename__ = "grade"

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True, comment="Grade ID")
    name = Column(String(25), nullable=False, unique=True, index=True, comment="Name of the academic grade")
    tag = Column(String(10), unique=True, nullable=False, comment="Short tag/abbreviation for the grade")
    level_id = Column(
        SmallInteger,
        ForeignKey("level.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="ID of the associated educational level",
    )

    level = relationship("Level", back_populates="grades")
    sections = relationship("Section", back_populates="grade")
