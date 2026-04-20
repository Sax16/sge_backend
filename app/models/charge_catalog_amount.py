from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class ChargeCatalogAmount(Base):
    """
    ChargeCatalogAmount model representing the precise amount of a charge mapped to an economic level.
    """
    __tablename__ = "charge_catalog_amount"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Charge Catalog Amount ID")
    charge_catalog_id = Column(Integer, ForeignKey("charge_catalog.id", ondelete="CASCADE"), nullable=False, index=True, comment="Charge Catalog ID")
    economic_level_id = Column(Integer, ForeignKey("economic_level.id", ondelete="SET NULL"), index=True, comment="Economic Level ID")
    amount = Column(Numeric(10, 2), nullable=False, comment="Amount")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    charge_catalog = relationship("ChargeCatalog", back_populates="amounts")
    economic_level = relationship("EconomicLevel", back_populates="charge_catalog_amounts")
