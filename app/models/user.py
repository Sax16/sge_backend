from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import func

from app.models.base import Base


class User(Base):
    """
    User model to represent user accounts in the system.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        user_name (str): Unique username for the user, used for login.
        password (str): Hashed password for user authentication.
        is_active (bool): Flag to indicate if the user account is active.
        created_at (datetime): Timestamp when the user account was created.
        employee_id (int): Foreign key to the associated employee record.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="User ID")
    user_name = Column(String(25), nullable=False, unique=True, index=True, comment="Username of the user")
    password = Column(String(255), nullable=False, comment="Password of the user")
    is_active = Column(Boolean, nullable=False, default=True, server_default="true", comment="Active status of the user")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Creation timestamp of the user")
    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        index=True,
        comment="ID of the associated employee",
    )

    employee = relationship("Employee", back_populates="user")
