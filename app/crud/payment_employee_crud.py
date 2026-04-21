from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.payment_employee import PaymentEmployee
from app.schemas.payment_employee import PaymentEmployeeCreate, PaymentEmployeeUpdate


def create_payment_employee(db: Session, payment_employee_in: PaymentEmployeeCreate) -> PaymentEmployee:
    payment_employee = PaymentEmployee(**payment_employee_in.model_dump())
    db.add(payment_employee)
    db.commit()
    db.refresh(payment_employee)
    return payment_employee


def get_payment_employee(db: Session, payment_employee_id: int | str) -> PaymentEmployee | None:
    return db.query(PaymentEmployee).filter(PaymentEmployee.id == payment_employee_id).first()


def get_payment_employees(db: Session, skip: int = 0, limit: int = 100) -> Sequence[PaymentEmployee]:
    return db.query(PaymentEmployee).order_by(PaymentEmployee.id).offset(skip).limit(limit).all()


def update_payment_employee(
    db: Session, payment_employee: PaymentEmployee, payment_employee_in: PaymentEmployeeUpdate
) -> PaymentEmployee:
    data = payment_employee_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(payment_employee, key, value)
    db.add(payment_employee)
    db.commit()
    db.refresh(payment_employee)
    return payment_employee


def delete_payment_employee(db: Session, payment_employee: PaymentEmployee) -> None:
    db.delete(payment_employee)
    db.commit()
