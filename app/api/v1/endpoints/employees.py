from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.crud.employee import (
    create_employee,
    delete_employee,
    get_employee,
    get_employees,
    update_employee,
)
from app.dependencies import get_db
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate


router = APIRouter()


@router.post(
    "", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED
)
def create_employee_endpoint(
    employee_in: EmployeeCreate, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = create_employee(db, employee_in)
    return employee


@router.get("", response_model=list[EmployeeRead])
def list_employees_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[EmployeeRead]:
    employees = get_employees(db, skip=skip, limit=limit)
    return list(employees)


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee_endpoint(
    employee_id: int, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return employee


@router.put("/{employee_id}", response_model=EmployeeRead)
def update_employee_endpoint(
    employee_id: int, employee_in: EmployeeUpdate, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    updated = update_employee(db, employee, employee_in)
    return updated


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee_endpoint(
    employee_id: int, db: Session = Depends(get_db)
) -> Response:
    employee = get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    delete_employee(db, employee)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
