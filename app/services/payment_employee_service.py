from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.payment_employee import PaymentEmployee
from app.schemas.payment_employee import PaymentEmployeeCreate, PaymentEmployeeUpdate
from app.crud import payment_employee_crud


def get_payment_employee(db: Session, payment_employee_id: int | str) -> PaymentEmployee | None:
    return payment_employee_crud.get_payment_employee(db, payment_employee_id)


def get_payment_employees(db: Session, skip: int = 0, limit: int = 100) -> Sequence[PaymentEmployee]:
    return payment_employee_crud.get_payment_employees(db, skip=skip, limit=limit)


def create_payment_employee(db: Session, payment_employee: PaymentEmployeeCreate) -> PaymentEmployee:
    return payment_employee_crud.create_payment_employee(db, payment_employee)


def update_payment_employee(db: Session, payment_employee: PaymentEmployee, payment_employee_in: PaymentEmployeeUpdate) -> PaymentEmployee:
    return payment_employee_crud.update_payment_employee(db, payment_employee, payment_employee_in)


def delete_payment_employee(db: Session, payment_employee: PaymentEmployee) -> None:
    payment_employee_crud.delete_payment_employee(db, payment_employee)
