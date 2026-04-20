from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class ChargeCatalog(Base):
    """
    ChargeCatalog model representing catalog of charges/fees.
    """
    __tablename__ = "charge_catalog"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Charge Catalog ID")
    name = Column(String(50), nullable=False, comment="Charge name")
    is_active = Column(Boolean, nullable=False, default=True, server_default="true", comment="Is charge active")

    amounts = relationship("ChargeCatalogAmount", back_populates="charge_catalog")
    payment_schedules = relationship("PaymentSchedule", back_populates="charge_catalog")
