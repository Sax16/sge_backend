from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Grade(Base):
    """
    Grade model representing academic grades (e.g., 1st grade, 2nd grade).

    Attributes:
        id (int): Primary key, auto-incremented unique identifier.
        name (str): Full name of the grade, must be unique.
        tag (str): Short tag/abbreviation for the grade, unique.
    """
    __tablename__ = "grades"

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True, comment="Grade ID")
    name = Column(String(25), nullable=False, unique=True, index=True, comment="Name of the academic grade")
    tag = Column(String(10), unique=True, nullable=False, comment="Short tag/abbreviation for the grade")

    sections = relationship("Section", back_populates="grade")
