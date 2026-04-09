from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Level(Base):
    """
    Level model representing educational levels (e.g., Primary, Secondary).

    Attributes:
        id (int): Primary key, auto-incremented unique identifier.
        name (str): Full name of the educational level, must be unique.
        modular_code (str): Modular code assigned to the level, optional.
        tag (str): Short tag/abbreviation for the level, unique.
    """
    __tablename__ = "levels"

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True, comment="Level ID")
    name = Column(String(25), nullable=False, unique=True, index=True, comment="Name of the educational level")
    modular_code = Column(String(20), unique=True, comment="Modular code for the level")
    tag = Column(String(10), unique=True, nullable=False, comment="Short tag/abbreviation for the level")

    sections = relationship("Section", back_populates="level")
