from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate



def get_expense(db: Session, expense_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id).first() 


def get_expenses(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Expense]:
    return db.query(Expense).order_by(Expense.id).offset(skip).limit(limit).all()


def create_expense(db: Session, expense_in: ExpenseCreate, user_id: int) -> Expense:
    expense_data = expense_in.model_dump()
    expense_data["user_id"] = user_id
    expense = Expense(**expense_data)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def update_expense(
    db: Session, expense: Expense, expense_in: ExpenseUpdate
) -> Expense:
    data = expense_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(expense, key, value)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense: Expense) -> None:
    db.delete(expense)
    db.commit()