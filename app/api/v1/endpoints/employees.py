from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.crud.employee import (
    create_employee as create_employee_crud,
    delete_employee as delete_employee_crud,
    get_employee as get_employee_crud,
    get_employees as get_employees_crud,
    update_employee as update_employee_crud,
)
from app.dependencies import get_db
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate


router = APIRouter()


@router.post(
    "", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED,
    description="Create a new employee"
)
def create_employee(
    employee_in: EmployeeCreate, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = create_employee_crud(db, employee_in)
    return employee


@router.get("", response_model=list[EmployeeRead], description="List all employees")
def get_employees(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[EmployeeRead]:
    employees = get_employees_crud(db, skip=skip, limit=limit)
    return list(employees)


@router.get("/{employee_id}", response_model=EmployeeRead, description="Get an employee by ID")
def get_employee(
    employee_id: int, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = get_employee_crud(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeRead, description="Update an employee by ID")
def update_employee(
    employee_id: int, employee_in: EmployeeUpdate, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = get_employee_crud(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    updated = update_employee_crud(db, employee, employee_in)
    return updated


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete an employee by ID")
def delete_employee(
    employee_id: int, db: Session = Depends(get_db)
) -> Response:
    employee = get_employee_crud(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    delete_employee_crud(db, employee)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
