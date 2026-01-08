from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(25), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        index=True,
    )

    employee = relationship("Employee", back_populates="user")
