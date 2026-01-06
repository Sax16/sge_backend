from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    dni = Column(String(15), nullable=False, unique=True, index=True)
    ruc = Column(String(15), unique=True, index=True)
    gender = Column(String(10), nullable=False)
    birth_date = Column(Date)
    phone_number = Column(String(15))
    email = Column(String(50), index=True)
    is_active = Column(Boolean, nullable=False)
    position = Column(String(50), nullable=False)
    address = Column(String(75))
    create_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="employee", uselist=False)
