from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class EconomicLevel(Base):
    """
    EconomicLevel model representing socioeconomic levels.
    """
    __tablename__ = "economic_level"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Economic Level ID")
    name = Column(String(15), nullable=False, unique=True, comment="Level name")
    description = Column(String(75), comment="Detailed description")

    students = relationship("Student", back_populates="economic_level")
    charge_catalog_amounts = relationship("ChargeCatalogAmount", back_populates="economic_level")
