from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import expense_service
from app.dependencies import get_db, check_super_admin, check_admin_or_super_admin, get_current_user
from app.schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.schemas.user import UserRead

router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])

@router.get("/{expense_id}", response_model=ExpenseRead, description="Get an expense by ID")
def get_expense(
    expense_id: int, db: Session = Depends(get_db)
) -> ExpenseRead:
    expense = expense_service.get_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.get("", response_model=list[ExpenseRead], description="Get all expenses")
def get_expenses(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ExpenseRead]:
    expenses = expense_service.get_expenses(db, skip=skip, limit=limit)
    return list(expenses)


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED, description="Create a new expense")
def create_expense(
    expense_in: ExpenseCreate, 
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
) -> ExpenseRead:
    expense = expense_service.create_expense(db, expense_in, user_id=current_user.id)
    return expense


@router.put(
    "/{expense_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update an expense by ID"
)
def update_expense(
    expense_id: int, expense_in: ExpenseUpdate, db: Session = Depends(get_db)
) -> Response:
    expense = expense_service.get_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    expense_service.update_expense(db, expense, expense_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete an expense by ID")
def delete_expense(
    expense_id: int, db: Session = Depends(get_db),
    current_user: UserRead = Depends(check_super_admin),
) -> Response:
    expense = expense_service.get_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    expense_service.delete_expense(db, expense)
    return Response(status_code=status.HTTP_204_NO_CONTENT)