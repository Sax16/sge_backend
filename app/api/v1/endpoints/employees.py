from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import employee_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{employee_id}", response_model=EmployeeRead, description="Get an employee by ID")
def get_employee(
    employee_id: int, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = employee_service.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.get("", response_model=list[EmployeeRead], description="List all employees")
def get_employees(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[EmployeeRead]:
    employees = employee_service.get_employees(db, skip=skip, limit=limit)
    return list(employees)


@router.post(
    "", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED,
    description="Create a new employee"
)
def create_employee(
    employee_in: EmployeeCreate, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = employee_service.create_employee(db, employee_in)
    return employee


@router.put("/{employee_id}", response_model=EmployeeRead, description="Update an employee by ID")
def update_employee(
    employee_id: int, employee_in: EmployeeUpdate, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = employee_service.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    updated = employee_service.update_employee(db, employee, employee_in)
    return updated


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete an employee by ID")
def delete_employee(
    employee_id: int, db: Session = Depends(get_db)
) -> Response:
    employee = employee_service.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    try:
        employee_service.delete_employee(db, employee)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return Response(status_code=status.HTTP_204_NO_CONTENT)
