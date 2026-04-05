from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.crud import employee_crud


def get_employee(db: Session, employee_id: int) -> Employee | None:
    return employee_crud.get_employee(db, employee_id)


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Employee]:
    return employee_crud.get_employees(db, skip=skip, limit=limit)


def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
    # verificar si el empleado ya existe
    existing_employee = employee_crud.get_employee_by_dni(db, employee.dni)
    if existing_employee:
        raise HTTPException(status_code=400, detail="There is an employee with the same DNI")

    # TODO: Implementar reglas de negocio
    
    return employee_crud.create_employee(db, employee)


def update_employee(db: Session, employee: Employee, employee_in: EmployeeUpdate) -> Employee:
    return employee_crud.update_employee(db, employee, employee_in)


def delete_employee(db: Session, employee: Employee) -> None:
    employee_crud.delete_employee(db, employee)
