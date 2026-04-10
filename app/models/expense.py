from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import ExpenseType
from app.models.base import Base


class Expense(Base):
    """
    Expense model representing institutional expenses.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier.
        name (str): Short description or name of the expense.
        amount (Decimal): Expense amount, max 6 digits, 2 decimals.
        date (date): Date when the expense occurred.
        expense_type (ExpenseType): Type/Category of the expense (enum).
        details (str): Additional details or long description of the expense.
        user_id (int): Foreign key to the User who registered or is responsible for the expense.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp of the last update.
    """
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Expense ID")
    name = Column(String(100), nullable=False, comment="Short description or name of the expense")
    amount = Column(Numeric(precision=6, scale=2), nullable=False, comment="Expense amount")
    date = Column(Date, nullable=False, comment="Date when the expense occurred")
    expense_type = Column(Enum(ExpenseType), nullable=False, comment="Type/Category of the expense")
    details = Column(String(255), comment="Additional details or long description")
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="ID of the user who registered the expense",
    )
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    user = relationship("User", back_populates="expenses")
