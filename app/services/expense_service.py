from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.crud import expense_crud


def get_expense(db: Session, expense_id: int) -> Expense | None:
    return expense_crud.get_expense(db, expense_id)


def get_expenses(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Expense]:
    return expense_crud.get_expenses(db, skip=skip, limit=limit)


def create_expense(db: Session, expense: ExpenseCreate, user_id: int) -> Expense:
    return expense_crud.create_expense(db, expense, user_id)


def update_expense(db: Session, expense: Expense, expense_in: ExpenseUpdate) -> Expense:
    return expense_crud.update_expense(db, expense, expense_in)


def delete_expense(db: Session, expense: Expense) -> None:
    expense_crud.delete_expense(db, expense)
