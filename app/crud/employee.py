from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(db: Session, employee_in: EmployeeCreate) -> Employee:
    employee = Employee(**employee_in.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_employee(db: Session, employee_id: int) -> Employee | None:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Employee]:
    return db.query(Employee).order_by(Employee.id).offset(skip).limit(limit).all()


def update_employee(
    db: Session, employee: Employee, employee_in: EmployeeUpdate
) -> Employee:
    data = employee_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(employee, key, value)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee: Employee) -> None:
    db.delete(employee)
    db.commit()
