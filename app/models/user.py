from sqlalchemy import SmallInteger
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy import func

from app.core.enums import UserRole
from app.models.base import Base


class User(Base):
    """
    User model to represent user accounts in the system.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        username (str): Unique username for the user, used for login.
        password (str): Hashed password for user authentication.
        is_active (bool): Flag to indicate if the user account is active.
        created_at (datetime): Timestamp when the user account was created.
        employee_id (int): Foreign key to the associated employee record.
    """
    __tablename__ = "user"

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True, comment="User ID")
    username = Column(String(25), nullable=False, unique=True, index=True, comment="Username of the user")
    password = Column(String(255), nullable=False, comment="Password of the user")
    is_active = Column(Boolean, nullable=False, default=True, server_default="true", comment="Active status of the user")
    role = Column(Enum(UserRole), nullable=False, default=UserRole.ADMIN, server_default=UserRole.ADMIN.value, comment="Role of the user")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Creation timestamp of the user")
    employee_id = Column(
        SmallInteger,
        ForeignKey("employee.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        index=True,
        comment="ID of the associated employee",
    )

    employee = relationship("Employee", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    enrollments = relationship("Enrollment", back_populates="user")
    charges = relationship("Charge", back_populates="user")
    receipts = relationship("Receipt", back_populates="user")
    employee_payments = relationship("PaymentEmployee", back_populates="user")